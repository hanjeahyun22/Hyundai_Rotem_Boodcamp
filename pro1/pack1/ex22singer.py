# class라는 설계도만 갖고 있는 파일

class Singer:
    title_song = "빛나라 대한민국"

    def sing(self):
        msg = "노래는 "
        print(msg, self.title_song)