using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CymbalVoice : MonoBehaviour
{


	public AudioSource audio_player;
	public AudioClip Cymbal_Front;
	public AudioClip Cymbal_Left;
	public AudioClip Cymbal_Right;


	// Use this for initialization
	void Start()
	{

	}

	// Update is called once per frame
	void Update()
	{

	}

	public void Play_music(byte[] finger_input)
	{
		var bits = new BitArray(finger_input);
		if (bits[0]) { audio_player.PlayOneShot(Cymbal_Right); Debug.Log("cymbal side"); }
		if (bits[1]) { audio_player.PlayOneShot(Cymbal_Front); Debug.Log("cymbal front"); }
		if (bits[2]) { audio_player.PlayOneShot(Cymbal_Left); Debug.Log("cymbal side"); }
	}


}

