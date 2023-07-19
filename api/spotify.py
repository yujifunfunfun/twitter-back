import spotipy
import statistics

client_id = '38b54d4b43a147bd91ef481871d06a04'
client_secret = 'fa9d974e5fd944148cd01f1e1b1c1f8a'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_audio_features(track_id):
    audio_features = sp.audio_features(track_id)
    return audio_features[0]


def get_audio_info(playlist_id):
    user = "315o2nxb7wdqctyyczjqb2ql27o4"
    list_title_artist = []
    list_track_name = []
    list_track_artist = []
    list_track_url = []
    list_track_id = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        list_title_artist.append(item)
    for title_artist in list_title_artist:
        track_name = title_artist['track']['name']
        track_url = title_artist['track']['external_urls']['spotify']
        track_artist = title_artist['track']["artists"][0]["name"]
        track_id = title_artist['track']['id']
        list_track_name.append(track_name)
        list_track_url.append(track_url)
        list_track_id.append(track_id)
        list_track_artist.append(track_artist)
    return list_track_name, list_track_id, list_track_url, list_track_artist


def analyse_playlist(playlist_id):
    danceability_list = []
    energy_list = []
    key_list = []
    loudness_list = []
    mode_list = []
    speechiness_list = []
    acousticness_list = []
    instrumentalness_list = []
    liveness_list = []
    valence_list = []
    tempo_list = []
    time_signature_list = []
    audio_features_list = []
    list_track_name, list_track_id, list_track_url, list_track_artist = get_audio_info(playlist_id)
    for track_id in list_track_id:
        audio_features = get_audio_features(track_id)
        audio_features_list.append(audio_features)
    for audio_features in audio_features_list:
        danceability_list.append(audio_features['danceability'])
        energy_list.append(audio_features['energy'])
        key_list.append(audio_features['key'])
        loudness_list.append(audio_features['loudness'])
        mode_list.append(audio_features['mode'])
        speechiness_list.append(audio_features['speechiness'])
        acousticness_list.append(audio_features['acousticness'])
        instrumentalness_list.append(audio_features['instrumentalness'])
        liveness_list.append(audio_features['liveness'])
        valence_list.append(audio_features['valence'])
        tempo_list.append(audio_features['tempo'])
        time_signature_list.append(audio_features['time_signature'])

    danceability_mean = round(statistics.mean(danceability_list) * 100)
    energy_mean = round(statistics.mean(energy_list) * 100)
    key_mean = round(statistics.mean(key_list), 2)
    loudness_mean = round(statistics.mean(loudness_list), 2)
    mode_mean = round(statistics.mean(mode_list), 2)
    speechiness_mean = round(statistics.mean(speechiness_list) * 100)
    acousticness_mean = round(statistics.mean(acousticness_list) * 100)
    instrumentalness_mean = round(statistics.mean(instrumentalness_list) * 100)
    liveness_mean = round(statistics.mean(liveness_list) * 100)
    valence_mean = round(statistics.mean(valence_list) * 100)
    tempo_mean = round(statistics.mean(tempo_list), 2)
    time_signature_mean = round(statistics.mean(time_signature_list), 2)

    audio_features_mean = [acousticness_mean, danceability_mean, energy_mean, instrumentalness_mean, key_mean, liveness_mean, loudness_mean, mode_mean, speechiness_mean, tempo_mean, time_signature_mean, valence_mean]
    return audio_features_mean


def search_audio_from_playlist(track_id, playlist_id):
    audio_features = get_audio_features(track_id)
    playlist_audio_features_list = []
    list_track_name, list_track_id, list_track_url, list_track_artist = get_audio_info(playlist_id)
    for track_id in list_track_id:
        playlist_audio_features = get_audio_features(track_id)
        playlist_audio_features_list.append(playlist_audio_features)

    similar_audio_list = []
    for  playlist_audio_features,track_name, track_url, track_artist in zip(playlist_audio_features_list, list_track_name, list_track_url, list_track_artist):
        if (abs(audio_features['acousticness'] - playlist_audio_features['acousticness']) <= 0.01 * min(audio_features['acousticness'], playlist_audio_features['acousticness'])
            and abs(audio_features['danceability'] - playlist_audio_features['danceability']) <= 0.01 * min(audio_features['danceability'], playlist_audio_features['danceability'])
            and abs(audio_features['energy'] - playlist_audio_features['energy']) <= 0.01 * min(audio_features['energy'], playlist_audio_features['energy'])
            and abs(audio_features['instrumentalness'] - playlist_audio_features['instrumentalness']) <= 0.01 * min(audio_features['instrumentalness'], playlist_audio_features['instrumentalness'])
            and abs(audio_features['key'] - playlist_audio_features['key']) <= 0.01 * min(audio_features['key'], playlist_audio_features['key'])
            and abs(audio_features['liveness'] - playlist_audio_features['liveness']) <= 0.01 * min(audio_features['liveness'], playlist_audio_features['liveness'])
            and abs(audio_features['loudness'] - playlist_audio_features['loudness']) <= 0.01 * abs(min(audio_features['loudness'], playlist_audio_features['loudness']))
            and abs(audio_features['mode'] - playlist_audio_features['mode']) <= 0.01 * min(audio_features['mode'], playlist_audio_features['mode'])
            and abs(audio_features['speechiness'] - playlist_audio_features['speechiness']) <= 0.01 * min(audio_features['speechiness'], playlist_audio_features['speechiness'])
            and abs(audio_features['tempo'] - playlist_audio_features['tempo']) <= 0.01 * min(audio_features['tempo'], playlist_audio_features['tempo'])
            and abs(audio_features['time_signature'] - playlist_audio_features['time_signature']) <= 0.01 * min(audio_features['time_signature'], playlist_audio_features['time_signature'])
            and abs(audio_features['valence'] - playlist_audio_features['valence']) <= 0.01 * min(audio_features['valence'], playlist_audio_features['valence'])
            ):
            similar_audio_list.append([track_name, track_url, track_artist])
    if len(similar_audio_list) == 0:
        similar_audio_list.append(["None"])

    return similar_audio_list
