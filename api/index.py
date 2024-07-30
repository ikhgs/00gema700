from groq import Groq
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Récupère le paramètre 'ask' depuis la requête GET
    ask = request.args.get('ask')
    if ask:
        # Crée une instance du client Groq
        client = Groq()
        # Appelle l'API de completion de chat de Groq
        completion = client.chat.completions.create(
            model="gemma-7b-it",
            messages=[
                {
                    "role": "user",
                    "content": ask
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Concatène les chunks de réponse en une seule chaîne
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        return jsonify({"response": response})
    else:
        return "Veuillez fournir une question dans le paramètre 'ask'. Exemple : /?ask=Citer les différents articles défini et indéfini avec des exemples et explications"

if __name__ == '__main__':
    # L'application écoute sur l'hôte 0.0.0.0 et le port 3400
    app.run(host='0.0.0.0', port=3400)
