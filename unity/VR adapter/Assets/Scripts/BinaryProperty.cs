using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BinaryProperty : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    public DataManagerScript managerScript;

    public string key;
    public string value_on;
    public string value_off;

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SendValue(bool state)
    {
        managerScript.SetKey(key);
        managerScript.SetValue(state ? value_on : value_off);
        managerScript.Send();
    }


}
