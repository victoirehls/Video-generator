style = "bangers,80,&H0008bdfb,&H00000000,&00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

stylemask = "bangers,80,&H00FFFFFF,&H00000000,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"

####
class Text:
    """Class defining an image caracterised by :
        - its content(string)
        - its style
        - its maskstyle (same style but white)
        - its beginning time in frames
        - its end time in frames
        """

    def __init__(self, content, style = style, stylemask = stylemask,  beginning=0, end=0):
        self.content = content
        self.style = style
        self.stylemask = stylemask
        self.beginning = 0
        self.end = 0



    def setBeginning(self, beginning):
        self.beginning = beginning

    def setEnd(self, end):
        self.end = end

    def setStyle(self,style):
        self.style = style

    def setStylemask(self,stylemask):
        self.stylemask = stylemask


