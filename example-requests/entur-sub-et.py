import datetime
import uuid
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree

# post request to Entur API for Estimated Timetable data
def lambda_handler(event, context):
    now = str(datetime.datetime.now()) + "+02:00"
    messageId = str(uuid.uuid1())
    messageId2 = str(uuid.uuid1())
    url = 'https://api.entur.org/anshar/1.0/subscribe/RUT'
    my_element = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Siri version="2.0" xmlns="http://www.siri.org.uk/siri" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns3="http://www.ifopt.org.uk/ifopt" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0">
    <SubscriptionRequest>
        <RequestTimestamp>''' + now + '''</RequestTimestamp>
        <RequestorRef></RequestorRef>
        <MessageIdentifier>''' + messageId + '''</MessageIdentifier>
        <ConsumerAddress></ConsumerAddress>
        <SubscriptionContext>
            <HeartbeatInterval>PT30S</HeartbeatInterval>
        </SubscriptionContext>
        <VehicleMonitoringSubscriptionRequest>
            <SubscriberRef></SubscriberRef>
            <SubscriptionIdentifier></SubscriptionIdentifier>
            <InitialTerminationTime></InitialTerminationTime>
            <VehicleMonitoringRequest version="2.0">
                <RequestTimestamp>''' + now + '''</RequestTimestamp>
                <MessageIdentifier>''' + messageId2 + '''</MessageIdentifier>
                <PreviewInterval>PT24H</PreviewInterval>
            </VehicleMonitoringRequest>
        </VehicleMonitoringSubscriptionRequest>
    </SubscriptionRequest>
</Siri>'''
    req = urllib.request.Request(url=url,
                                data=my_element.encode(),
                                headers={'Accept': 'application/xml',
                                        'Content-Type': 'application/xml',
                                        'ET-Client-Name': ''
                                        })
    response = urllib.request.urlopen(req)
    the_page = response.read()

    # TODO implement
    return {
        'statusCode': response.status,
        'body': print('Siri data received')
    }
