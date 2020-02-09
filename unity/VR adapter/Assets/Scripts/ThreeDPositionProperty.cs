using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ThreeDPositionProperty : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    public DataManagerScript DataManager;
    public string CollideEnterExitKey;
    public string CollideEnterValue;
    public string CollideExitValue;

    public string LocationXKey;
    public string LocationYKey;
    public string LocationZKey;

    // Update is called once per frame
    void Update()
    {
        ;
    }


    private void OnTriggerEnter(Collider other)
    {
        DataManager.SetKey(CollideEnterExitKey);
        DataManager.SetValue(CollideEnterValue);
        DataManager.Send();
    }

    private void OnTriggerExit(Collider other)
    {
        DataManager.SetKey(CollideEnterExitKey);
        DataManager.SetValue(CollideExitValue);
        DataManager.Send();
    }

    public Transform DebugFactor;

    private void OnTriggerStay(Collider other)
    {
        Vector3 min = GetComponent<Collider>().bounds.min;
        Vector3 max = GetComponent<Collider>().bounds.max;
        Vector3 loc = other.bounds.center;
        Vector3 factor = new Vector3(
            Mathf.InverseLerp(min.x, max.x, loc.x),
            Mathf.InverseLerp(min.y, max.y, loc.y),
            Mathf.InverseLerp(min.z, max.z, loc.z)
            );

        if (DebugFactor)
        {
            DebugFactor.position = factor;
        }

        DataManager.Send(LocationXKey, factor.x.ToString());
        DataManager.Send(LocationYKey, factor.y.ToString());
        DataManager.Send(LocationZKey, factor.z.ToString());
    }
}
