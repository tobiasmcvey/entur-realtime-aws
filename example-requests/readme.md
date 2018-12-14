# Example-requests

These are examples from Entur for sending POST requests to **start** and **terminate** subscriptions.

We can **start our subsription** with a POST request. I recommend using **[Postman](https://www.getpostman.com/)** to test this first.

We can also **terminate a request**. This is useful when testing our architecture's ability to monitor and heal an interrupted or timed out request.

For both kinds of requests we want a unique `MessageIdentifier` for each request. We use the [uuid library](https://docs.python.org/3/library/uuid.html) in python for this, and [datetime](https://docs.python.org/3/library/datetime.html) for generating our timestamps dynamically.

In case our subscription fails due to errors on our end or the supplier Entur, we can use the same `SubscriptionIdentifier` to restart our subscription and pick up the data we missed between the last and next API request. 

For that reason we want to keep this stored as a string.

**Start subscription for Estimated Timetable**

entur-subscription-et.xml

```XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Siri version="2.0" xmlns="http://www.siri.org.uk/siri" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns3="http://www.ifopt.org.uk/ifopt" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0">
	<SubscriptionRequest>
		<RequestTimestamp></RequestTimestamp>
		<Address></Address>
		<RequestorRef></RequestorRef>
		<MessageIdentifier></MessageIdentifier>
		<SubscriptionContext>
			<HeartbeatInterval>PT30S</HeartbeatInterval>
		</SubscriptionContext>
		<EstimatedTimetableSubscriptionRequest>
			<SubscriberRef></SubscriberRef>
			<SubscriptionIdentifier></SubscriptionIdentifier>
			<InitialTerminationTime></InitialTerminationTime>
			<EstimatedTimetableRequest version="2.0">
				<RequestTimestamp></RequestTimestamp>
				<MessageIdentifier></MessageIdentifier>
			</EstimatedTimetableRequest>
		</EstimatedTimetableSubscriptionRequest>
	</SubscriptionRequest>
</Siri>
```
| Fields | Role |
| -------------------- | ------------------- |
| `RequestTimestamp` | Time for start of our subscription in UTC, UNIX timestamp |
| `Address` | The URL for our endpoint to receive data | 
| `RequestorRef` | The name of the requestor |
| `MessageIdentifier` | Unique identifier for each message. Should always be unique. |
| `HeartbeatInterval` | Time-interval for desired delivery of data. 30 seconds is currently minimum at Entur |
| `SubscriptionIdentifier` | The unique ID for the subscription. Keep this so you can restart a terminated subscription and recover data from down-time. |
| `InitialTerminationTime` | The date to end our subscription, UNIX timestamp |

**Start subscription for Vehicle Monitoring**

entur-subscription-vm.xml

```XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Siri version="2.0" xmlns="http://www.siri.org.uk/siri" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns3="http://www.ifopt.org.uk/ifopt" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0">
    <SubscriptionRequest>
        <RequestTimestamp></RequestTimestamp>
        <RequestorRef></RequestorRef>
        <MessageIdentifier></MessageIdentifier>
        <ConsumerAddress></ConsumerAddress>
        <SubscriptionContext>
            <HeartbeatInterval>PT30S</HeartbeatInterval>
        </SubscriptionContext>
        <VehicleMonitoringSubscriptionRequest>
            <SubscriberRef></SubscriberRef>
            <SubscriptionIdentifier></SubscriptionIdentifier>
            <InitialTerminationTime></InitialTerminationTime>
            <VehicleMonitoringRequest version="2.0">
                <RequestTimestamp></RequestTimestamp>
                <MessageIdentifier></MessageIdentifier>
                <PreviewInterval>PT24H</PreviewInterval>
            </VehicleMonitoringRequest>
        </VehicleMonitoringSubscriptionRequest>
    </SubscriptionRequest>
</Siri>
```

| Fields | Role |
| -------------------- | ------------------- |
| `RequestTimestamp` | Time for start of our subscription in UTC, UNIX timestamp |
| `ConsumerAddress` | The URL for our endpoint to receive data | 
| `RequestorRef` | The name of the requestor |
| `MessageIdentifier` | Unique identifier for each message. Should always be unique. |
| `HeartbeatInterval` | Time-interval for desired delivery of data. 30 seconds is currently minimum at Entur |
| `SubscriptionIdentifier` | The unique ID for the subscription. Keep this so you can restart a terminated subscription and recover data from down-time. |
| `InitialTerminationTime` | The date to end our subscription, UNIX timestamp |


**Terminate subscription for SubscriptionIdentifier**

entur-subscription-termination.xml

```XML
<?xml version="1.0" encoding="UTF-8"?>
<Siri version="1.4" xmlns="http://www.siri.org.uk/siri" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns3="http://www.ifopt.org.uk/ifopt" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0">
    <TerminateSubscriptionRequest>
        <RequestTimestamp></RequestTimestamp>
        <RequestorRef></RequestorRef>
        <MessageIdentifier></MessageIdentifier>
        <SubscriptionRef></SubscriptionRef>
    </TerminateSubscriptionRequest>
</Siri>
```

| Fields | Role |
| -------------------- | ------------------- |
| `RequestTimestamp` | Time for start of our subscription in UTC, UNIX timestamp |
| `RequestorRef` | The name of the requestor |
| `MessageIdentifier` | Unique identifier for each message. Should always be unique. |
| `SubscriptionRef` | The unique ID for the subscription. Keep this so you can restart a terminated subscription and recover data from down-time. |


