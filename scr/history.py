class history:
    urls = []
    current_index = 0
    cut = 0
    def get(self, position): #position +1 or -1
        pos = self.current_index + position
        if pos <= 0 or pos > len(self.urls):
            return
        self.current_index += position
        self.cut += position
        print(self.urls[self.current_index-1])
        return self.urls[self.current_index-1]
    def set(self, link, scroll, select=0):
        sorted(self.urls, key=lambda key: key[0])

        while self.cut < 0:
            try:
                del self.urls[-1]
                self.cut += 1
                self.current_index -= 1
            except:
                pass

        try:
            self.urls[self.current_index][2] = scroll
        except:
            pass#self.urls[2] = 0
        self.current_index = len(self.urls)
        self.urls.append([self.current_index, link, 0, select])
        self.current_index += 1
