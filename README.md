## **Real-time SIRI data on AWS**

This is an architecture for streaming public transport data for Norway from Entur on Amazon Web Services. **[Entur](https://en-tur.no)** is the national trip-planner, ticket and transport information service provider in Norway.

Entur provides the following topics for scheduled and real-time public transit information

| Data-type | Contents |
| ------------ | --------- |
| Estimated Timetable | Timetables with planned, actual and expected departure times for public transport |
| Situation Exchange | Text messages for end-users about departure times, specific routes and stops |
| Vehicle Monitoring | Real-time location of public transport buses, trams and trains on their route, including deviations |

**[Entur for Developers](https://www.entur.org/dev/sanntidsdata/)** supplies us with an API for these topics and allows us to extract them as separate streams and segment by supplier. The data is structured in the [SIRI](https://en.wikipedia.org/wiki/Service_Interface_for_Real_Time_Information) XML standard.

We can narrow down the data-type for a specific area. For this example we can get data from the local provider called **[Ruter](https://ruter.no)**. 

Here are the steps: 

We will establish subscriptions for each data-type using a separate endpoint for each data-type. Then we will convert it into a simpler format, JSON, to prepare it for analysis and ingestion into other streaming and database types such as Kinesis, Elasticsearch or any other service of choice. 

API Gateway expects JSON so we **need** a mapping template to turn the XML into a JSON object.

Hopefully this will help you create similar loosely coupled microservices in [Amazon Web Services](https://aws.amazon.com/) and other cloud-based platforms like [Google Cloud](https://cloud.google.com/) and [Microsoft Azure](https://azure.microsoft.com/).

Enjoy!

### **Components**

* [API Gateway](https://aws.amazon.com/api-gateway/) for our endpoints and API management
* [Lambda](https://aws.amazon.com/lambda/) for starting subscriptions and handling responses from Entur
* [Cloudwatch](https://aws.amazon.com/cloudwatch/) [Logs, Metrics and Alarms](https://aws.amazon.com/cloudwatch/features/) for logging, debugging and alarms when our subscriptions time out
* [Kinesis](https://aws.amazon.com/kinesis/) for streaming our data into other services of choice
* [Simple Notification Service (SNS)](https://aws.amazon.com/sns/) for notifying our lambda functions when we need to restart a subscription

### **Architecture**

![alt text](https://github.com/tobmcv/Real-time-SIRI-data-on-AWS/blob/master/pictures-links/Overview%20architecture.png "Overview of Architecture")

#### Setup in this order

1. API Gateway resources for each data-type: VM, ET, SX
2. Lambda-functions for POST requests to each data-type
3. Kinesis streams for each data-type
4. Lambda for transforming response from Entur, one for each data-type
5. SNS topics for each data-type
6. Cloudwatch Metrics and Alarms for each data-type

We recommend setting up enough resources to handle each data-type separately, since it is possible that only one data-type subscription gets terminated. We want the architecture to continue running on any active subscriptions, and to restart only when one is terminated.

### **How it works**

Step by step, this is how the architecture works

#### **Establish a subscription**
We use API Gateway to setup our endpoint to receive data. We use the URL for our endpoint resources as our `ConsumerAddress` when making POST requests to Entur. This defines the address Entur will stream data to. 

We setup 3 resources, one for each data-type we want. For example, 'endpoint-vm' could be a resource name for our Vehicle Monitoring stream, 'endpoint-et' could be used for Estimated Timetable and so on. We only need the POST method for these endpoints.

We can now setup a lambda to send POST requests. We can use the [urrllib.request library](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) for this. See the example-requests section for the XML body to send with each request.

In order to receive and transform the response from Entur we must prepare the endpoint to handle XML. API Gateway expects JSON so we need a mapping template to turn the XML into a JSON object. 

[This example from Peter Fox](https://medium.com/@SlyFireFox/tips-and-hacks-for-working-with-aws-lambda-and-api-gateway-803403866abe) lets us fetch the body of the XML as input to a JSON object. All we need to do is parse it and turn it into any desired format. This example assumes JSON is preferable. 

To set this on the Integration Request in AWS Console, go to 

> API Gateway > APIs > YourAPIname > Resources > Method(POST) > Integration Request > Mapping Templates

configure **Request body passthrough** to **When there are no templates defined (recommended)** and set content-type as `application/xml`, and paste in

```
{
    "body" : $input.json('$')
}
```

See the [Amazon docs](http://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-mapping-template-reference.html#input-variable-reference) if you want to map the data differently.

We can now use Lambda for *both* starting our subscriptions and transforming the data returned by Entur. We will use separate lambda functions for each task though to avoid creating a loop.

#### **Transform data**
The API Gateway is also a trigger for our lambda function's code, so the code will run when new data arrives at our endpoint address.

This is the step where we will convert the data from the public standard SIRI XML format into a simpler JSON object format. We can simply convert it into JSON, or flatten it and remove SIRI head properties as well. 

After the data is ready, we send it to Kinesis so it can be streamed to other services of choice. 

To do this you need a policy and a suitable role for executing lambda, using Cloudwatch logs and Kinesis. I recommend creating a custom role for this with limited scopes.

We also log both the converted dataset and the `HeartbeatNotification` from Entur. The heartbeat tells us that the subscription is active and the timestamp for when Entur sends us their response. We use this in our next step for monitoring.

Here is an example in Python
```Python
import json
import xmltodict

def lambda_handler(event, context):
    print("Received event")
    siri_data = xmltodict.parse(event["body"])
    #print(siri_data)

    json_string = json.dumps(siri_data)
    # json string
    print(json_string)
    
    # TODO implement
    return {
        'statusCode': '200',
        'body': 'Siri data received'
    }

```

#### **Monitor subscription**
Using Cloudwatch logs, we will setup Metrics and Alarms to track when the `HeartbeatNotification` from Entur expires, and when it is not delivered in a 5-minute interval.

Our Cloudwatch Alarm takes a Metric as input, so we need to define this. See the [Amazon docs on filters]() to understand how you can build a filter and define a metric.

**Defining our Cloudwatch Metric**

We need only to see if there is a HeartbeatNotification, but assuming Entur does deliver it when the subscription is terminated, we will also look for changes in the property of the heartbeat's status. Here is a filter

```
{ $.HeartbeatNotification.Status = true }
```

Our metric will increment a count value every time this value appears in our logs. We set this increment to 1. 

**Defining our Cloudwatch Alarm**

Now we are ready to define an alarm based on the metric. We can set a threshold value to trigger the alarm, and decide how the alarm should interpret the metric value, and any actions we want it to take. 

We set the rule to trigger when there is less than 1 count of our metric every 5 minutes.

Next, our options for interpreting the threshold are 

* Good (not breaching threshold)
* Bad (breaching threshold)
* Missing (maintain the alarm state)

We can set this to Bad (breaching threshold), and we are going to use this as a signal to restart our subscription. Here's how:

We set the Alarm to publish a notification to an SNS topic for the data-type we are missing.  

Note that because we don't have dynamic variables in Cloudwatch we cannot simply define an alarm trigger when there are more than 5 minutes between each heartbeat. We must use static values. 

If you want to act on the contents of a Cloudwatch log you can instead define a [Cloudwatch Event](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html) and send this to a service such as Lambda to parse the log content.

#### **Restart subscription**
For each data-type we define a SNS topic. Once an SNS topic receives a message, they invoke a Lambda function to start our subscription to the Entur API again.

To do this, setup an SNS topic in the console and create a subscription. Set the subscription protocol to AWS Lambda, and specify which lambda function to call.

For this final step we want to point the SNS topic to the first lambda function that sends the POST request to Entur. 

These last 2 steps provide us with a monitoring and automation component to our microservice architecture. Instead of losing data, we can restart the subscription using the same ID and get any lost data upon the next delivery from Entur. 


#### **Example requests**

To test the API see the [Example requests section](https://github.com/tobmcv/Real-time-SIRI-data-on-AWS/tree/master/example-requests) for example code to run in AWS lambda and an explanation of the Siri XML responses.

POST requests
* **entur-sub-et.py**
* **entur-sub-vm.py**
Code for Lambda functions to subscribe to and collect data from entur.org/dev/sanntidsdata

These scripts send our POST requests to [Entur's API](https://www.entur.org/dev/sanntidsdata/) for real-time data so we can start a subscription for a topic. The examples are for the topics **Vehicle Monitoring** and **Estimated Timetable**.

The POST request uses an XML payload. Set `RequestorRef` and `ET-Client-Name` to the name of your organisation. You can reuse the unique ID `SubscriptionIdentifier` if the subscription is terminated to recover lost data. The field `MessageIdentifier` should always be a random unique ID for each type of request. 

Handling responses
* **entur-res-et.py**
* **entur-res-vm.py**

These scripts listen to our endpoints for each topic and transforms the response data from XML to JSON, and removes the head properties from the [SIRI standard](https://en.wikipedia.org/wiki/Service_Interface_for_Real_Time_Information).

The script also has a function for posting data straight to a Kinesis data stream in AWS, and handling for the `HeartbeatNotification`. This can be watched to monitor the health of a subscription, or replaced with another service of choice.


**With thanks to**

**[Lasse Tyrihjell](https://github.com/lassetyr)** who explained Entur's API

**[Christoffer Solem](https://github.com/csolem)** who helped solve data transformation
