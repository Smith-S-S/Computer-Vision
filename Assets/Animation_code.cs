using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
using System.Threading;
public class Animation_code : MonoBehaviour

{
    public GameObject[] Body;
    List<string> lines;
    int counter =0;
    // Start is called before the first frame update
    void Start()
    {
        lines= System.IO.File.ReadLines("Assets/Animation.txt").ToList(); //taking the file and converting 
        //into list
        
    }

    // Update is called once per frame
    void Update()
    {
        //print(lines[0]);
        string[] points=lines[counter].Split(','); //taking the 1st point
        //print(points[0]);
        for (int i=0; i<=32;i++)
        {
            float x=float.Parse(points[0+(i*3)])/100; //here we convert the string to float because unity have small 
            //number but we got large num
            //0 then 3 then 6
            float y=float.Parse(points[1+(i*3)])/100; // here 1,4
            float z=float.Parse(points[2+(i*3)])/100; // 2, 5
            Body[i].transform.localPosition=new Vector3(x,y,z);

        }
        
        counter +=1;

        if (counter==lines.Count) {counter=0;}
        //basicall it check how many lines have in the 
        //text file
        Thread.Sleep(30);

    }
}
