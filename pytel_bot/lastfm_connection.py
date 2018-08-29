import pylast
from pytel_bot.tokens import get_tokens
from datetime import datetime


class LastFM(object):
    def __init__(self):
        tokens = get_tokens()
        api_key = tokens['api_key']
        api_secret = tokens['shared_secret']
        self.__network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)

    @property
    def network(self):
        return self.__network

    def get_last_tracks(self, number_of_tracks: int, user: str) -> str:
        try:
            recent_pylast_tracks = self.network.get_user(user).get_recent_tracks(limit=number_of_tracks + 1)
            recent_str_tracks = 'Lista de las últimas {} canciones escuchadas de {}\n\n'.format(number_of_tracks, user)
            count = 0
            for track in recent_pylast_tracks:
                count += 1
                ago = (datetime.now().timestamp() // 1 - int(track.timestamp)) // 60
                recent_str_tracks += str(
                    count) + '\t ' + track.track.get_artist().get_name() + ' - ' + track.track.get_title() + '\t\t\t hace ' + str(
                    ago) + ' minutos\n'
        except pylast.WSError:
            recent_str_tracks = 'Usuario no encontrado :('
        return recent_str_tracks

    def get_now_playing(self, user: str) -> str:
        try:
            track = self.network.get_user(user).get_now_playing()
            if track:
                text = '{} está escuchando ahora '.format(
                    user) + track.get_title() + ' de ' + track.get_artist().get_name()
            else:
                text = 'El usuario no está escuchando nada haora mismo :('
        except pylast.WSError:
            text = 'Usuario no encontrado :('
        return text

    def get_playcount(self, user: str) -> str:
        try:
            user = self.network.get_user(user)
            register = datetime.fromtimestamp(int(user.get_registered()))
            text = 'El usuario {} ha hecho {} scrobblings desde {} del {} de {}\n'.format(
                user, user.get_playcount(), register.day, register.month, register.year
            )
        except pylast.WSError:
            text = 'Usuario no encontrado'
        return text
