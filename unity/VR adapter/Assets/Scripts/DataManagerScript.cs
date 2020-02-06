using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using UnityEngine;

public class DataManagerScript : MonoBehaviour
{

    UdpClient udpClient;
    IPEndPoint remote;
    // Start is called before the first frame update
    void Start()
    {
        udpClient = new UdpClient(port);
        remote = new IPEndPoint(IPAddress.Parse(IPAddr), port);
        udpClient.Connect(remote);
        udpClient.BeginReceive(new AsyncCallback(recv), null);
    }

    public string IPAddr;
    public enum protocol { UDP, };
    public protocol ConnectionProtocol = protocol.UDP;
    public int port;


    // Update is called once per frame
    void Update()
    {
    }

    void recv(IAsyncResult res)
    {
        var recieved = udpClient.EndReceive(res, ref remote);
        print(recieved);


        udpClient.BeginReceive(new AsyncCallback(recv), null);

    }

    string key, value;

    public void SetKey(string key)
    {
        this.key = key;
    }

    public void SetValue(string value)
    {
        this.value = value;
    }

    public void Send()
    {
        if(key == null | value == null) {
            print("Key or value is null??");
            this.key = null;
            this.value = null;
            return;
        }
        // TODO: maybe make async?
        List<Byte> bytes = new List<byte>();
        foreach (var character in key)
        {
            bytes.Add((byte)character);
        }
        bytes.Add(0xff);
        foreach (var character in value)
        {
            bytes.Add((byte)character);
        }
        bytes.Add(0x00);

        if (Debug.isDebugBuild)
        {
            string s = "";
            foreach (var chr in bytes)
            {
                s += (char)chr;
            }
            print(s);
        }
        udpClient.Send(bytes.ToArray(), bytes.Count);

        this.key = null;
        this.value = null;
    }
}
