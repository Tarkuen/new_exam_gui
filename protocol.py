import json


class Protocol:

    def __init__(self):
        self.keywords= {}
        with open('protocol.json', 'r') as f:
            keys = json.load(f)

        for k,v in keys.items():
            self.keywords.update({k:v})
        
    def getKeywords(self):
        return self.keywords

    def handle_private(self, **kwargs):

        msg = kwargs.get('msg')

        assert msg.find('{') != -1
        assert msg.find('}') != -1
        recievers = []

        start = msg.find('{')
        end = msg.find('}')

        submsg = msg[start+1 : end].split(',')

        for t in submsg:
            recievers.append(t.strip(',').strip(' '))
        
        submsg = msg[end+1:]

        return recievers, submsg

    def handle_quit(self, **kwargs):
        pass

    def handle_file(self, **kwargs):
        return "HANDLED FILE"

if __name__ == "__main__":
    p = Protocol()
    msg = "{jhon, heidi} @file"
    recievers = ['jhon', 'heidi']
    clients = ['jhon', 'heidi']

    [print(c+" (PRIVATE) "+rec) for rec in recievers for c in clients if rec==c]
           
           
        