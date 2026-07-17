# A__line Ember+ control — extracted from the User Guide V1.8 (ch. 9)


A__line User GuideVersion: 1.8.0/174/100
9. Remote Control (via Ember+)
9.     Remote Control (via Ember+)This chapter describes the Ember+ implementation.
9.1 IntroductionAll parameters within A__line devices are accessible via Ember+. This allows an external control system, such asa Lawo console or VSM, to remotely control or respond to parameter changes within the device. For example, toadjust an IO parameter or change the mapping of local IO signals to the TX/RX streams.
Ember+ is a non-proprietery TCP/IP protocol supported by a wide range of Lawo products. More details aboutthe Ember+ protocol can be found at https://github.com/Lawo/ember-plus/wiki
.
The rest of this chapter describes the Ember+ parameters and how they can be viewed.
9.2 Ember+ Tree ViewerThe Ember+ Tree Viewer can be used to check the status of Ember+ parameters and/or switch a parametermanually. This can be useful when configuring and testing an Ember+ controlled device. 
To use the application:
1. Download the ".bz2" or ".xz" archive from the location https://github.com/Lawo/ember-plus/releases
 andunzip it.
2. Navigate to the folder "tools" and unzip the file "EmberPlusView-X.X.X.zip"
3. Double-click on the file "EmberPlusView.exe" to start the Ember+ Tree Viewer.
4. Once the application is open, click on "Add.." to add a new communication port:
5. Enter the IP Address and Port number of your device.
For devices with a MGMT port, you can use any of the network interfaces: RAVENNA/AES67 or MGMT.
The port number should always be 9000.
6. Select OK to add the device to the Ember+ Viewer - the virtual status LED will turn green once the treehas been fully read.
7. You can now open the branches of the tree and select a parameter to interrogate or alter its status.

A__line User Guide Version: 1.8.0/1 75/100
9. Remote Control (via Ember+)
9.3 Ember+ Tree Structure
/system
Root node of the System module. It covers:
· Network settings
· Audio levels
/identity
Implements the de.l-s-b.emberplus.identity schema:
· product
· version
· role
· company
· serial
/log/severityFilter
Controls the verbosity of log output in NodeCtrl. 0 (trace) to 5 (fatal)
/sync
Root node for the sample rate and audio sync settings. The actual tree structure depends on the available syncsources of the system.
/ravenna
Root node for internal signal routing and streaming.
/ravenna/discovery
Root node for the discovery module, which collects available streams from the network.

A__line User GuideVersion: 1.8.0/176/100
9. Remote Control (via Ember+)
/ravenna/discovery/interfaces
A list of available audio interfaces, under which the available sessions/streams are being shown.
Example:
{
    "discovery":
    {
        "interfaces":
        {
            "strm0":
            {
                "streams":
                {
                    "RemoteStream1":
                    {
                        "sdp": [string, SDP of the remote stream],
                        "primarySource": [string, URL of the remote stream, or its primary URL incase of redundancy],
                        "secondarySource": [string, secondary URL, empty for non-redundant streams],
                    }
                }
            }
        }
    }
}
/ravenna/routing
Root node for the internal (assumed) mono signal matrix and streaming.
/ravenna/routing/functions
A collection of functions for stream and matrix configuration/manipulation.
/ravenna/routing/functions/settings
Contains some default settings that will be used by the functions.
/ravenna/routing/functions/createInputStream
Creates an internal handle for Rx streams.
Arguments:
{
    "interface": [string, audio interface to receive the stream],
    "id": [string, internal identifier of this stream, must be unique for this audio interface],
    "delay": [int, size of the jitter buffer for one channel of this stream in samples],
    "syntonized": [bool, syntonized or synchronized mode] 
}
Return Values:
{
    "errorText": [string, empty on success]
}

A__line User Guide Version: 1.8.0/1 77/100
9. Remote Control (via Ember+)
/ravenna/routing/functions/deleteInputStream
Deletes an internal Rx stream handle.
Arguments:
{
    "interface": [string, audio interface the stream was received from],
    "id": [string, internal identification of the stream],
}
Return Values:
{
    "errorText": [string, empty on success]
}
/ravenna/routing/functions/resetInputStatistics
Resets accumulated statistics. The path can be of length 0, 1 or 2 in order to address all inputs, an audiointerface or a stream.
Arguments:
{
    "inputPath": [string, "", "[interface]" oder "[interface]/[id]"]
}
Return Values:
{
    "errorText": [guess what]
}
/ravenna/routing/functions/createOutputStream
Creates a new Tx stream. 'Stream' in this context solely reserves outputs of the internal mono matrix. In order toactually stream to the network, 'senders' must be added to the stream ('createOutputStreamSender').
Arguments:
{
    "interface": [string, audio interface],
    "streamId": [string, internal key of this stream],
    "channelCount": [int, number of channels in this stream]
}
Return Values:
{
    "errorText": [.]
}

A__line User GuideVersion: 1.8.0/178/100
9. Remote Control (via Ember+)
/ravenna/routing/functions/createOutputStreamSender
Creates a Rx sender for an existing stream.
Arguments:
{
    "interface": [string, audio interface of the stream],
    "streamId": [string, internal key of the stream],
    "senderId": [string, internal key of the sender, must be unique within this stream],
    "primaryAddress": [string, ip address, or empty for ' multicast auto', the address range impliesthe distinction between unicast and multicast],
    "primaryPort": [int, port number, only relevant for unicast],
    "usePrimary": [bool, true if primaryAddress/-Port should be used]
    "secondaryAddress": [string, must logically correspond to 'primaryAddress'],
    "secondaryPort": [int],
    "useSecondary": [bool, true if secondaryAddress/-Port should be used]
    "dscp": [int],
    "codec": [int, 0=L16, 1=L24, 2=L32, 3=AM824],
    "frameSize": [int, number of samples per channel and frame],
    "ttl": [int, "time to live"]
}
Return Values:
{
    "errorText": [string]
}
/ravenna/routing/functions/deleteOutputStreamSender
Deletes a Tx sender.
Arguments:
{
    "interface": [string, audio interface],
    "streamId": [string, internal key of the Tx stream of the sender to delete],
    "senderId": [string, internal key of the sender to be deleted]
}
Return Values:
{
    "errorText": [string]
}
/ravenna/routing/functions/deleteOutputStream
Deletes a Tx stream and all its senders.
Arguments:
{
    "interface": [string, audio interface],
    "streamId": [string]
}
Return Values:
{
    "errorText": [string]
}

A__line User Guide Version: 1.8.0/1 79/100
9. Remote Control (via Ember+)
/ravenna/routing/functions/connectChannel
Sets or clears one mono connection in the internal matrix. If the destination was already connected, thatconnection will be discarded.
Arguments:
{
    "outputPath": [string, "[medium]/[channel]" oder "[audio interface]/[stream]/[channel]"],
    "inputPath": [string, "[medium]/[channel]" oder "[audio interface]/[stream]/[channel]"]
}
Return Values:
{
    "errorText": [string]
}
Example:
{
    "outputPath": "strm0/myTxStream0/3",
    "inputPath": "madi0/63" 
}
/ravenna/routing/functions/subscribeURLs
Allows both redundant RTSP-URLs to be automatically set for an existing Rx stream.
Arguments:
{
    "interface": [string, audio interface],
    "streamId": [string],
    "primary": [string, primary URL],
    "secondary" [string, secondary URL]
}
Return Values:
{
    "errorText": [string]
}
/ravenna/routing/functions/saveRouting
Experimental.

A__line User GuideVersion: 1.8.0/180/100
9. Remote Control (via Ember+)
/ravenna/routing/inputs
Hierarchical representation of the input axis of the internal mono matrix. Streaming and non-streaming devicescan be distinguished by their device root node's schema identifiers.
Schema-Identifiers are one of:
· com.lawo.ravenna.inputs.streaming
· com.lawo.ravenna.inputs.medium
Example:
{
    "inputs":
    {
        [Example of a streaming device]
        "strm0":
        {
            "streams": [list of Rx stream representations]
            {
                "MyRxStream1":
                {
                    [TBD]
                }
            }
        },
        [Example of a non-streaming device]
        "madi0":
        {
            "channelCount": 64
        }
    }
}    
The matrix inputs serve solely as a reference for what exists. Connections are being established at the outputs.
/ravenna/routing/outputs
Hierarchical representation of the output axis of the internal mono matrix. Streaming and non-streaming devicescan be distinguished by their device root node's schema identifiers.
Schema-Identifiers are one of:
· com.lawo.ravenna.inputs.streaming
· com.lawo.ravenna.inputs.medium
Example:
{
    "outputs":
    {
        [example of a streaming device]
        "strm0":
        {
            "streams": [List of existing Tx streams]
            {
                [Example of a 2-channel Tx stream]
                "MyTxStream1":
                {
                    "channels":
                    {
                        "_0":
                        {
                            "track": 0, [internal information]

A__line User Guide Version: 1.8.0/1 81/100
9. Remote Control (via Ember+)
                            "input": "strm0/MyRxStream1/0" [Channel 0 of "MyRxStream1" at "strm0" isrouted to this output channel]
                        },
                        "_1":
                        {
                            "track": 1, [interne Information]
                            "input": "madi/0" [Channel 0 of "madi0" is routed to this output channel]
                        }
                    },
                    "senders": [A stream can be streamed from any number of senders with differingsettings]
                    {
                        "Sender1":
                        {
                            [TBD]
                        }
                    }
                }
            }
        },
        [Example for a non-streaming device]
        "madi0":
        {
            "_0":
            {
                "input": "strm0/MyRxStream1/0" [Channel 0 of "MyRxStream1" at "strm0" is routed tothis output channel]
            },
            "_1":
            {
                "input": "madi/0" [Channel 0 of "madi0" is routed to this output channel]
            },
            [62 more MADI output channels]
        }
    }
} 
/ravenna/facades
Root node for alternative views of the data.
/IoControl/Facades/UnifiedNumbering/
This facade provides a reduced view/access to the A__stage IoControl part of the ember+ tree. The nodenumbers in this facade are fixed and do not change between systems starts. Control of the resources remainsthe same as described in the respective ember+ schema.
/warmstart
Settings that control nodectrl's behaviour while restarting.
/warmstart/writeData
Writes the data tree's current state to a file so that it can be restored at the next start.
/warmstart/autoSaveInterval
Controls periodic storage of Warmstart data, in seconds. 0 means 'off'. 
Please use with care, as this may take a significant time and cause the system to slow down periodically.

A__line User GuideVersion: 1.8.0/182/100
9. Remote Control (via Ember+)
/warmstart/forceColdstart
Forces a cold start of the system by deleting warmstart data.
/config
Root node of an experimental system configuration module.
/IoControl/Boards
Base node for control of I/O (-board) parameters
/IoControl/Boards/_<board_index>
Sub node with control parameters of one board.
/IoControl/Boards/_<board_index>/General
Contains read only common information about the I/O board.
· Available: avaliable state; True: communication with I/O board is active; False: communication with I/Oboard is disturbed or impossible.
· ResetFlags: representation of internal reset flags. For development purposes only.
· Clock/Config: system clock configuration (0: 44100, 1:48000, 2: 88200, 3: 96000)
· Clock/State: internal clock state flags. For development purposes only.
· Fpga/Done: FPGA state; True: FPGA is booted; False: FPGA not booted.
· Fpga/Identity: internal code of FPGA file type
· HwInfo/IdentityRegister: representation of internal identity data. For development purposes only.
· HwInfo/CardIdentity: identification number of I/O board.
· HwInfo/HwRev: hardware revision.
· HwInfo/PcbRev: printed circuit board revision.
/IoControl/Boards/_<board_index>/GpIn
If an I/O board provides general purpose inputs, this node is present. If GPI is not provided, this node is notpresent.
· _<GpIn_index>: index of the input.
For I/O boards with GPI resources, an additional control may be provided:
/IoControl/Boards/_<board_index>/GpIn/Run: activate (true) or deactivate (false) monitoring of inputs
Schema-Identifier:
· com.lawo.emberplus.gpin.v1.0
Ember+ schema documentation of this resource can be found onhttps://github.com/Lawo/ember-plus/wiki/Schema-Definition:-com.lawo.emberplus.gpin-(Version-1)

A__line User Guide Version: 1.8.0/1 83/100
9. Remote Control (via Ember+)
/IoControl/Boards/_<board_index>/GpOut
If an I/O board provides general purpose outputs, this node is present. If GPO is not provided, this node is notpresent.
· _<GpOut_index>: index of the output.
Schema-Identifier:
· com.lawo.emberplus.gpout.v1.0
Ember+ schema documentation of this resource can be found athttps://github.com/Lawo/ember-plus/wiki/Schema-Definition:-com.lawo.emberplus.gpout-(Version-1)
/IoControl/Boards/_<board_index>/InputChannels/_<channel_index>
If an I/O board provides parameters for input channels, this node is present. If there are no input channels orno parameters for provided input channels, this node is not present.
The following input resource types may be found if the board provides them:
/IoControl/Boards/_<board_index>/InputChannels/_<channel_index>/MicLineSchema-Identifier:
· com.lawo.emberplus.micline.v2.0
Ember+ schema documentation of this resource can be found athttps://github.com/Lawo/ember-plus/wiki/Schema-Definition:-com.lawo.emberplus.micline-(Version-2)
For I/O boards with MicLine resources, an additional state information may be provided:
/IoControl/Boards/_<board_index>/InputChannels/P48Generator: board wide 48V phantom powergenerator is active (true) or not (false)
The active state here is a prerequisite for the activation of phantom power on individual channels as describedin the schema identifier.
/IoControl/Boards/_<board_index>/InputChannelPairs/_<channel_pair_index>
If an I/O board provides control parameters valid for a pair of input channels simultaneously (e.g. AES3In), thisnode is present. If not, this node is not present.
The following input resource types may be found if the board provides them:
/IoControl/Boards/_<board_index>/InputChannels/_<channel_pair_index>/Aes3Schema-Identifier:
· com.lawo.emberplus.aes3in.v1.0
Ember+ schema documentation of this resource can be found athttps://github.com/Lawo/ember-plus/wiki/Schema-Definition:-com.lawo.emberplus.aes3in-(Version-1)
/IoControl/Boards/_<board_index>/OutputChannels/_<channel_index>
If an I/O board provides parameters for output channels, this node is present. If there are no output channels orno parameters for provided output channels, this node is not present.
The following output resource types may be found if the board provides them:
/IoControl/Boards/_<board_index>/OutputChannels/_<channel_index>/LineSchema-Identifier:
· com.lawo.emberplus.lineout.v1.0
Ember+ schema documentation of this resource can be found athttps://github.com/Lawo/ember-plus/wiki/Schema-Definition:-com.lawo.emberplus.lineout-(Version-1)

A__line User GuideVersion: 1.8.0/184/100
9. Remote Control (via Ember+)
/IoControl/Boards/_<board_index>/OutputChannelPairs/_<channel_pair_index>
If an I/O board provides control parameters valid for a pair of output channels simultaneously (e.g. AES3Out),this node is present. If not, this node is not present.
The following input resource types may be found if the board provides them:
/IoControl/Boards/_<board_index>/OutputChannelPairs/_<channel_pair_index>/Aes3Schema-Identifier:
· com.lawo.emberplus.aes3out.v1.0
Ember+ schema documentation of this resource can be found athttps://github.com/Lawo/ember-plus/wiki/Schema-Definition:-com.lawo.emberplus.aes3out-(Version-1)

A__line User Guide Version: 1.8.0/1 85/100
9. Remote Control (via Ember+)
9.4 Working with the Ember+ Tree
9.4.1 Receiving a Stream
Receiving a stream in nodectrl has two parts:
· Creating an input stream representation.
· Subscribing to a session.
In some applications, the stream representation can be reused by subscribing to a different session.
Create an input stream
In order to create a synchronized input stream (representation) called 'MyIn0' at audio interface 'strm0' with asample buffer of 32 samples per channel, call:
ravenna/routing/functions/createInputStream ("strm0", "MyIn0", 32, false)
Subscribe by SDP
Set:
/ravenna/routing/inputs/strm0/streams/MyIn0/sourceSDP
to your desired source session SDP.
Ø To choose a (non-redundant) stream from the session, set:
/ravenna/routing/inputs/strm0/streams/MyIn0/primaryStreamIndex
to the desired stream index of the session. 0 by default.
Ø To choose a redundant stream from the session, set:
/ravenna/routing/inputs/strm0/streams/MyIn0/primaryStreamIndex
/ravenna/routing/inputs/strm0/streams/MyIn0/secondaryStreamIndex
to the desired stream indices of the session. 0 and -1 by default.
Subscribe by RTSP-URL
Call:
/ravenna/routing/functions/subscribeURLs ("strm0", "MyIn0", [primary], [secondary])
to set your desired SDP sources. [secondary] may be an empty string for a non-redundant RTSP-URL, or asecondary source URL.
Unsubscribe from a stream
It is recommended (but not enforced) that you unsubscribe in the same fashion you subscribed.
Ø To unsubscribe by SDP, set:
/ravenna/routing/inputs/strm0/MyIn0/sourceSDP
to "".
Ø To unsubscribe by RTSP, call:
/ravenna/routing/functions/subscribeURLs ("strm0", "MyIn0", "", "")
Delete an input stream
Call:
/ravenna/routing/functions/deleteInputStream ("strm0", "MyIn0")
Any ongoing subscription will be implicitly unsubscribed.

A__line User GuideVersion: 1.8.0/186/100
9. Remote Control (via Ember+)
9.4.2 Sending a Stream
Sending a stream in nodectrl has two parts:
· Creating an output stream representation.
· Adding sender(s) to the stream representation.
In some applications, multiple senders with differing parameters might be added to a stream, using matrixresources only once.
Create an output stream
In order to create an output stream with 2 channels called "MyOut0" at audio interface "strm0", call:
ravenna/routing/functions/createOutputStream ("strm0", "MyOut0", 2)
Add a sender
In order to add a sender called "theSender" to "MyOut0" at "strm0", call:
/ravenna/routing/functions/createOutputStreamSender ("strm0", "MyOut0", "theSender", ...) 
with the desired sender-specific parameters.
Remove a sender
Call:
/ravenna/routing/functions/deleteOutputStreamSender ("strm0", "MyOut0", "theSender")
Delete an output stream
Call:
/ravenna/routing/functions/deleteOutputStream ("strm0", "MyOut0")
All remaining senders will be implicitly removed.
9.4.3 Connecting Inputs to Outputs
In order to connect channel 0 of input medium "madi0" to channel 0 in output stream "MyOut0" at audiointerface "strm0", call:
/ravenna/routing/functions/connectChannel ("strm0/MyOut0/0", "madi0/0")
You can also connect the following devices: streaming to non-streaming, non-streaming to non-streaming orstreaming to streaming.
9.4.4 Disconnecting Outputs
In order to disconnect channel 0 in output stream "MyOut0" at audio interface "strm0", call:
/ravenna/routing/functions/connectChannel ("strm0/MyOut0/0", "")
9.4.5 Manipulating IO ParametersThis section describes how state values and control parameters of audio IO and GPIO resources arerepresented in the Ember+ tree.
Locating IO Parameters
On devices with audio IO and/or GPIO resources, the Ember+ tree structure represents the physical appearanceof the device.

A__line User Guide Version: 1.8.0/1 87/100
9. Remote Control (via Ember+)
Resource controls are grouped in nodes which represent the IO boards, each having an index node in the tree.Index _0 is typically the main board.
"root" node of state and control parameters of mainboard resources:
/IoControl/Boards/_0
The other indices enumerate the IO boards which are physically present in a unit from the board at the top (index_1) to the bottom.
The resource parameters of an IO board are grouped in the nodes InputChannels, OutputChannels, GpIn andGpOut with channel or channel pair indices.
The tree contains only nodes for resources which are present on a board AND have state data or controllableparameters.
Example
Abstract of the IoControl tree from a unit with a main board containing GPIO, one AES3 board, one LineOutboard and one MicLine board:
{    "IoControl":    {        "Boards":        {            "_0":            {                "GpIn":                {                    "_0":                    {                        [GP In state]                    },                    "_1":                    {                        [GP In state]                    },                    [more general purpose inputs]                },                "GpOut":                {                    "_0":                    {                        [GP Out state/control parameters]                    },                    "_1":                    {                        [GP Out state/control parameters]                    },                    [more general purpose outputs]                }            },            "_1":            {                "InputChannelPairs":                {                    "_0":                    {                        "Aes3":                         {                            [AES3In channel pair state/control parameters]                        }                    },                    "_1":                    {                        "Aes3":                         {                            [AES3In channel pair state/control parameters]                        }                    },                    [more AES3 input channel pairs]

A__line User GuideVersion: 1.8.0/188/100
9. Remote Control (via Ember+)
                }            },            "_2":            {                "OutputChannels":                {                    "_0":                    {                        "Line":                        {                            [LineOut channel state/control parameters]                        }                    },                    "_1":                    {                        "Line":                        {                            [LineOut channel state/control parameters]                        }                    },                    [more LineOut channels]                }            },            "_3":            {                "InputChannels":                {                    "_0":                    {                        "MicLine":                        {                            [MicLine channel state/control parameters]                        }                    },                    "_1":                    {                        "MicLine":                        {                            [MicLine channel state/control parameters]                        }                    },                    [more MicLine channels]                }            }        }    }}

A__line User Guide Version: 1.8.0/1 89/100
10. Appendices
10.     AppendicesThis chapter includes further information which you may find useful.
10.1 Part Numbers
System Component
Part Number
A__stage48
3RU, 16 mic/line, 16 line out, 8 AES3 IO, 1 red. MADI, 8 GPIO
985/60
A__stage64
4RU, 32 mic/line, 16 line out, 8 AES3 IO, 1 red. MADI, 8 GPIO
985/62
A__stage80
3RU, 32 mic/line, 32 line out, 8 AES3 IO, 1 red. MADI, 8 GPIO
985/64
A__digital64
3RU, 32 AES3 IO, 1 red. MADI, 8 GPIO
985/63
A__madi6
1RU, 3 x AoIP to MADI converter.
985/23
SFPs (RAVENNA & MADI)
Please see the optional accessories
.
981/60-xx
Spare Parts
Internal PSU Block
436-7310-000
Internal Fan
350-3288-000
10.1.1 Data SheetsFurther technical information can be found in the product data sheets. The system part numbers will help youlocate the data sheets for the main system components. 
All documentation is available from the Downloads area at www.lawo.com
 (after Login).