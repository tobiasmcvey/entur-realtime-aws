# Example-responses

These are examples of response from Entur in both XML and JSON format.

**Heartbeat notification**

entur-heartbeatnotification.xml

```XML
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Siri version="2.0" xmlns="http://www.siri.org.uk/siri" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns3="http://www.ifopt.org.uk/ifopt" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0">
    <HeartbeatNotification>
        <RequestTimestamp></RequestTimestamp>
        <ProducerRef></ProducerRef>
        <Status>true</Status>
        <ServiceStartedTime></ServiceStartedTime>
    </HeartbeatNotification>
</Siri>
```

| Fields | Role |
| -------------------- | ------------------- |
| `RequestTimestamp` | Time Entur sent our heartbeat in UTC, UNIX timestamp |
| `ProducerRef` | The unique ID for the subscription. Keep this so you can restart a terminated subscription and recover data from down-time. |
| `Status` | The status of our subscription. Is either `true` or `false` |
| `ServiceStartedTime` | Time our subscription started in UTC, UNIX timestamp |

**Vehicle Monitoring Response in XML**

TBA

```XML

```

**Vehicle Monitoring Response in JSON**

TBA

```XML

```