using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;


public class TriggerTransmitterScript : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Squeeze.AddOnChangeListener(OnLeftSqueeze, LeftHand);
        Squeeze.AddOnChangeListener(OnRightSqueeze, RightHand);
        GrabPinch.AddOnChangeListener(OnLeftGrabPinch, LeftHand);
        GrabPinch.AddOnChangeListener(OnRightGrabPinch, RightHand);

    }

    private void OnLeftGrabPinch(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource, bool newState)
    {
        DataManager.Send(LeftGrabKey, newState ? GrabTrueValue : GrabFalseValue);
    }

    private void OnRightGrabPinch(SteamVR_Action_Boolean fromAction, SteamVR_Input_Sources fromSource, bool newState)
    {
        DataManager.Send(RightGrabKey, newState ? GrabTrueValue : GrabFalseValue);
    }

    private void OnLeftSqueeze(SteamVR_Action_Single fromAction, SteamVR_Input_Sources fromSource, float newAxis, float newDelta)
    {
        DataManager.Send(LeftSqueezeKey, newAxis.ToString());
    }

    private void OnRightSqueeze(SteamVR_Action_Single fromAction, SteamVR_Input_Sources fromSource, float newAxis, float newDelta)
    {
        DataManager.Send(RightSqueezeKey, newAxis.ToString());
    }


    public DataManagerScript DataManager;
    public SteamVR_Action_Boolean GrabPinch;
    public SteamVR_Action_Single Squeeze;
    public SteamVR_Input_Sources LeftHand, RightHand;

    public string LeftSqueezeKey, RightSqueezeKey, LeftGrabKey, RightGrabKey, GrabTrueValue, GrabFalseValue;

    // Update is called once per frame
    void Update()
    {
    }

}
