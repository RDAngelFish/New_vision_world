using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DrumVoice : MonoBehaviour {



	public AudioSource audio_player;
	public AudioClip drum_front;
	public AudioClip drum_side;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}


	public void Play_music(byte[] finger_input)
	{
		var bits = new BitArray(finger_input);
		if (bits[0]) { audio_player.PlayOneShot(drum_side); Debug.Log("drum side"); }
		if (bits[1]) { audio_player.PlayOneShot(drum_front); Debug.Log("drum front"); }
		if (bits[2]) { audio_player.PlayOneShot(drum_front); Debug.Log("drum front"); }
		if (bits[3]) { audio_player.PlayOneShot(drum_side); Debug.Log("drum side"); }
	}


}
