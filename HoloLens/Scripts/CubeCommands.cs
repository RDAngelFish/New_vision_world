
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Threading;
using System.Net.Sockets;
using System;
//using HoloToolkit.Unity.InputModule;

#if !UNITY_EDITOR
using System.IO;
using System.Threading.Tasks;
using Windows.Networking;
using Windows.Networking.Sockets;
#endif

public class CubeCommands : MonoBehaviour
{
    
    //private Material materialColored;
	PianoVoice piano;
	DrumVoice drum;
	CymbalVoice cymbal;

	public int test1 = 0;
	public int test2 = 0;
	public GameObject piano_object;
	public GameObject drum_object;
	public GameObject cymbal_object;
	public string HostName = "192.168.0.132";
    public string port = "9999";

    private bool isConnect = false;
    private bool _iskeepRun;
    string mes = "";
#if UNITY_EDITOR
    private TcpClient _client;
    private Thread _clientThread;
    public NetworkStream stream = null;
#else
    StreamSocket socket;
    private System.IO.StreamWriter writer = null;
    private Windows.Storage.Streams.DataReader reader = null;
    private Task _clientTask;


#endif
    private Queue _msgEventQueue = new Queue();
    private Mutex _msgEventQueueMutex = new Mutex();
    private string errorStatue;
    //private bool thread_close = true;

    // byte[] data = new byte[240];
    private void Start()
    {
		//isConnect = true;
		//connectToServer();       

		piano = GameObject.Find("VoiceControl").GetComponent<PianoVoice>();
		drum = GameObject.Find("VoiceControl").GetComponent<DrumVoice>();
		cymbal = GameObject.Find("VoiceControl").GetComponent<CymbalVoice>();
	}
 
    private void Update()
    {
        if (mes.Length != 0)
        {
            Debug.Log("mes: " + mes);
            mes = "";
        }
        if (_msgEventQueue.Count != 0)
        {
            _msgEventQueueMutex.WaitOne();
            while (_msgEventQueue.Count != 0)
            {
                byte[] args = (byte[])_msgEventQueue.Dequeue();
				var bits = new BitArray(args);
				int instrument_type = System.BitConverter.ToInt32(args, 0);
				//Debug.Log(instrument_type);
				if (bits[31])
				{
					piano_object.SetActive(true);
					drum_object.SetActive(false);
					cymbal_object.SetActive(false);
					piano.Play_music(args);
				}
				else if (bits[30])
				{
					drum_object.SetActive(true);
					piano_object.SetActive(false);
					cymbal_object.SetActive(false);
					drum.Play_music(args);
				}
				else if (bits[29])
				{
					cymbal_object.SetActive(true);
					piano_object.SetActive(false);
					drum_object.SetActive(false);
					cymbal.Play_music(args);
				}
					
			}
            _msgEventQueueMutex.ReleaseMutex();
        }

    }
	private void OnDestroy()
    {
        disconnectFromServer();
    }
	// Called by GazeGestureManager when the user performs a Select gesture
	void OnSelect()
	//void OnMouseUpAsButton()
    {
		{
            //Debug.Log("Click!");
            //materialColored = new Material(Shader.Find("Diffuse"));
            //materialColored.color = new Color(UnityEngine.Random.value, UnityEngine.Random.value, UnityEngine.Random.value);
            //this.GetComponent<Renderer>().material = materialColored;

//#if UNITY_EDITOR
//            if (materialColored != null)
//                UnityEditor.AssetDatabase.DeleteAsset(UnityEditor.AssetDatabase.GetAssetPath(materialColored));
//#endif
            if (!isConnect)
            {
				Debug.Log("try to connect");
				isConnect = true;
                connectToServer();
			}
            else
            {
				Debug.Log("try to disconnect");
				disconnectFromServer();
                isConnect = false;
            }
            //eventData.Use();
        }
    }
    public void connectToServer()
    {
#if UNITY_EDITOR
        _clientThread = new Thread(() => RunClient());
        _clientThread.Start();
#else
        Connect();
#endif
	}

#if !UNITY_EDITOR
    private async Task StartAccessAsync() {
        uint n = 1;
        uint size = n * 4;
        byte[] data = new byte[4*n]; // Buffer
                                     // byte[] data = new byte[400]; // Buffer
                                     //byte[] data1 = System.Text.Encoding.ASCII.GetBytes("L");
        char[] data1 = "Linku starto".ToCharArray();

        writer.Write(data1, 0, data1.Length);
        Debug.Log("[TCP Client] Connected");
        _iskeepRun = true;
        try
        {
            while (_iskeepRun)
            {
                await reader.LoadAsync(size);
                reader.ReadBytes(data);
                //mes += "size: " + data.Length;
                _msgEventQueueMutex.WaitOne();
                _msgEventQueue.Enqueue(data);
                _msgEventQueueMutex.ReleaseMutex();
            }
        }
        catch (SocketException e)
        {
            Debug.Log(e.Message);
        }
    }
    //private void StartAccess() {
    //    _clientTask = Task.Run(() => RunClient());
    //}
    private void Connect()
    {
        ConnectUWP();
    }
    private async void ConnectUWP()
    {
        errorStatue = "not UWP";
        mes = "start connect\n";
        try
        {
            socket = new Windows.Networking.Sockets.StreamSocket();
            Windows.Networking.HostName serverHost = new Windows.Networking.HostName(HostName);
            await socket.ConnectAsync(serverHost, port);
            writer = new StreamWriter(socket.OutputStream.AsStreamForWrite()) { AutoFlush = true };
            reader = new Windows.Storage.Streams.DataReader(socket.InputStream);

            mes += "connect down";
            await StartAccessAsync();

        }
        catch (Exception e)
        {
			 mes += "connect failed";
            errorStatue = e.ToString();
        }
    }
#endif

	void RunClient()
    {
#if UNITY_EDITOR
		_client = new TcpClient(HostName, 9999);
		Debug.Log("Begin");
		if (_client == null || !_client.Connected) {
            mes += ("link failed\n");
			Debug.Log("Failed");
			_client = null;
            return;
        }
        else
        {
          mes  += ("link success\n");
		  Debug.Log("Success");
		}
        // Get the socket stream
        stream = _client.GetStream();
        byte[] data = new byte[252]; // Buffer
       // byte[] data = new byte[400]; // Buffer
        byte[] data1 = System.Text.Encoding.ASCII.GetBytes("L"); 
        stream.Write(data1, 0, data1.Length);
        Debug.Log("[TCP Client] Connected");
        _iskeepRun = true;
        try
        {
            while (_iskeepRun)
            {
                
                if (_client.Available > 0)
                {
                    stream.Read(data, 0, data.Length);
                    mes += ("recv\n");
                    _msgEventQueueMutex.WaitOne();
                    _msgEventQueue.Enqueue(data);
                    _msgEventQueueMutex.ReleaseMutex();
                }
                else 
                {
                    if (_client.Client.Receive(data1, SocketFlags.Peek) == 0)
                        break;
                    Thread.Sleep(20);
                    continue;
                }
            }
			stream.Close();
            stream = null;
            _client.Close();
            _client = null;
        }
        catch (SocketException e)
        {
            Debug.Log(e.Message);
        }
#else
        mes += ("\n[TCP Client] Connected");
		Debug.Log("Hololens success");
        uint n = 4;
        uint size = n * 252;
        byte[] data = new byte[252*n]; // Buffer
                                     // byte[] data = new byte[400]; // Buffer
                                     //byte[] data1 = System.Text.Encoding.ASCII.GetBytes("L");
        char[] data1 = "Linku starto".ToCharArray();

        byte[] data_s = new byte[252];
        writer.Write(data1, 0, data1.Length);
        //Debug.Log("[TCP Client] Connected");
        _iskeepRun = true;
        try
        {
            while (_iskeepRun)
            {
                //mes += "length: " + reader.UnconsumedBufferLength + "\n";
                Task.Run(async() => {
                    await reader.LoadAsync(size);
                    reader.ReadBytes(data);
                    //mes += "size: " + data.Length;
                    for (int i = 0; i < n; i++)
                    {
                        System.Array.Copy(data, i * 252, data_s, 0, 252);
                        _msgEventQueueMutex.WaitOne();
                        _msgEventQueue.Enqueue(data_s);
                        _msgEventQueueMutex.ReleaseMutex();

                    }
                });
                //if (reader.UnconsumedBufferLength>0)
                //{
                //    reader.ReadBytes(data);
                //    mes += "size: " + data.Length;
                //    _msgEventQueueMutex.WaitOne();
                //    _msgEventQueue.Enqueue(data);
                //    _msgEventQueueMutex.ReleaseMutex();
                //}
                //else 
                //{
                //    Task.Run(async () => { await Task.Delay(2000); });
                //}
            }
            
        }
        catch (SocketException e)
        {
            Debug.Log(e.Message);
        }

#endif
	}

	public void disconnectFromServer()
    {
#if UNITY_EDITOR
		if (_client == null || !_client.Connected)
            return;

        _iskeepRun = false;
        _clientThread.Join();
        _clientThread = null; 
        Debug.Log("[TCP Client] Closed");
#else
        if (socket == null) return;
        _iskeepRun = false;
        reader.DetachBuffer();
        socket.Dispose();
        writer.Dispose();
        reader.Dispose();
        socket = null;
        writer = null;
        reader = null;
        Debug.Log("[TCP Client] Closed");
#endif
	}
}