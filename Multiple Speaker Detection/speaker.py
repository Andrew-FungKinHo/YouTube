# pip install --upgrade google-cloud-speech

# imports
import io
import os
from google.cloud import speech_v1p1beta1 as speech

def get_transcript(speech_file,content_type):
    # google authentication
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/andrewfung/Programming/Multiple Speaker Detection/multiple-speaker-detection-3ed65d50eff1.json'

    # wget -nc https://realenglishconversations.com/...

    # instantiate a speech client and declare an audio file
    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    if 'wav' in content_type:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_speaker_diarization=True,
            diarization_speaker_count=2,
        )
    elif 'mpeg' in content_type:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_speaker_diarization=True,
            diarization_speaker_count=2,
        )
    elif 'flac' in content_type:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_speaker_diarization=True,
            diarization_speaker_count=2,
        )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    result = response.results[-1]
    words_info = result.alternatives[0].words

    words_list = []
    # Printing out the output:
    for word_info in words_info:
        words_list.append(
            {
                'word': word_info.word,
                'speaker_tag': word_info.speaker_tag,
                'start_time': word_info.start_time,
                'end_time': word_info.end_time,
            }
        )
    # print(words_list)

    # create a script based on the words_list
    current_speaker = words_list[0]['speaker_tag']
    current_line = []
    script = []

    for item in words_list:
        if item['speaker_tag'] != current_speaker:
            # speaker changed, end of line
            script.append(
                {
                    'speaker': current_speaker,
                    'line': current_line
                }
            )
            current_line = []
            current_speaker = item['speaker_tag']
        else:
            # same speaker, add to the current line
            current_line.append(item['word'])

    script.append(
        {
            'speaker': current_speaker,
            'line': current_line
        }
    )

    script = [(f"Speaker {line['speaker']}: " + " ".join(line['line']) + "\n") for line in script]
    return script