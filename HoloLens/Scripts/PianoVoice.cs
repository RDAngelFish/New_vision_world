using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PianoVoice : MonoBehaviour {


	public AudioSource audio_player;
	public AudioClip piano_C1_1;
	public AudioClip piano_C1_2;
	public AudioClip piano_C1_3;
	public AudioClip piano_C1_4;
	public AudioClip piano_C1_5;
	public AudioClip piano_C1_6;
	public AudioClip piano_C1_7;
	public AudioClip piano_C2_1;
	public AudioClip piano_C2_2;
	public AudioClip piano_C2_3;
	public AudioClip piano_C2_4;
	public AudioClip piano_C2_5;
	public AudioClip piano_C2_6;
	public AudioClip piano_C2_7;
	public AudioClip piano_C3_1;
	public AudioClip piano_C3_2;
	public AudioClip piano_C3_3;
	public AudioClip piano_C3_4;
	public AudioClip piano_C3_5;
	public AudioClip piano_C3_6;
	public AudioClip piano_C3_7;
	public AudioClip piano_C4_1;
	public AudioClip piano_C4_2;
	public AudioClip piano_C4_3;
	public AudioClip piano_C4_4;
	public AudioClip piano_C4_5;
	public AudioClip piano_C4_6;
	public AudioClip piano_C4_7;


	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void Play_music(byte[] finger_input)
	{
		var bits = new BitArray(finger_input);
		if (bits[0]) { audio_player.PlayOneShot(piano_C1_1); Debug.Log("piano C1_1"); }
		if (bits[1]) { audio_player.PlayOneShot(piano_C1_2); Debug.Log("piano C1_2"); }
		if (bits[2]) { audio_player.PlayOneShot(piano_C1_3); Debug.Log("piano C1_3"); }
		if (bits[3]) { audio_player.PlayOneShot(piano_C1_4); Debug.Log("piano C1_4"); }
		if (bits[4]) { audio_player.PlayOneShot(piano_C1_5); Debug.Log("piano C1_5"); }
		if (bits[5]) { audio_player.PlayOneShot(piano_C1_6); Debug.Log("piano C1_6"); }
		if (bits[6]) { audio_player.PlayOneShot(piano_C1_7); Debug.Log("piano C1_7"); }
		if (bits[7]) { audio_player.PlayOneShot(piano_C2_1); Debug.Log("piano C2_1"); }
		if (bits[8]) { audio_player.PlayOneShot(piano_C2_2); Debug.Log("piano C2_2"); }
		if (bits[9]) { audio_player.PlayOneShot(piano_C2_3); Debug.Log("piano C2_3"); }
		if (bits[10]) { audio_player.PlayOneShot(piano_C2_4); Debug.Log("piano C2_4"); }
		if (bits[11]) { audio_player.PlayOneShot(piano_C2_5); Debug.Log("piano C2_5"); }
		if (bits[12]) { audio_player.PlayOneShot(piano_C2_6); Debug.Log("piano C2_6"); }
		if (bits[13]) { audio_player.PlayOneShot(piano_C2_7); Debug.Log("piano C2_7"); }
		if (bits[14]) { audio_player.PlayOneShot(piano_C3_1); Debug.Log("piano C3_1"); }
		if (bits[15]) { audio_player.PlayOneShot(piano_C3_2); Debug.Log("piano C3_2"); }
		if (bits[16]) { audio_player.PlayOneShot(piano_C3_3); Debug.Log("piano C3_3"); }
		if (bits[17]) { audio_player.PlayOneShot(piano_C3_4); Debug.Log("piano C3_4"); }
		if (bits[18]) { audio_player.PlayOneShot(piano_C3_5); Debug.Log("piano C3_5"); }
		if (bits[19]) { audio_player.PlayOneShot(piano_C3_6); Debug.Log("piano C3_6"); }
		if (bits[20]) { audio_player.PlayOneShot(piano_C3_7); Debug.Log("piano C3_7"); }
		if (bits[21]) { audio_player.PlayOneShot(piano_C4_1); Debug.Log("piano C4_1"); }
		if (bits[22]) { audio_player.PlayOneShot(piano_C4_2); Debug.Log("piano C4_2"); }
		if (bits[23]) { audio_player.PlayOneShot(piano_C4_3); Debug.Log("piano C4_3"); }
		if (bits[24]) { audio_player.PlayOneShot(piano_C4_4); Debug.Log("piano C4_4"); }
		if (bits[25]) { audio_player.PlayOneShot(piano_C4_5); Debug.Log("piano C4_5"); }
		if (bits[26]) { audio_player.PlayOneShot(piano_C4_6); Debug.Log("piano C4_6"); }
		if (bits[27]) { audio_player.PlayOneShot(piano_C4_7); Debug.Log("piano C4_7"); }
	}
}
