from flask import Flask, request, jsonify

from main import primary
from main import secondary
from numpy.core.defchararray import lower

app=Flask(__name__)

@app.route('/chat', methods=['GET', 'POST'])

def chatBotGreetings():
    chatInput = request.form['chatInput']
    response = primary(chatInput)
    followup = secondary(chatInput)
    errorfollowup = "Maaari mo bang itama ang iyong sinend?"

    if followup == "None":
        return jsonify({'chatBotReply':primary(chatInput),'chatBotReply2':errorfollowup})
    
    elif followup == None:
        return jsonify({'chatBotReply':primary(chatInput),'chatBotReply2':errorfollowup})
    
    else:
        return jsonify({'chatBotReply':primary(chatInput),'chatBotReply2':secondary(chatInput)})
        #reply = primary(chatInput) + " " + secondary(chatInput)
        #return jsonify(chatBotReply=reply)

if __name__ == '__main__':
    app.run(host='192.168.0.162', debug=True)
