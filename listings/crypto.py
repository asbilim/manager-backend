from Cryptodome.Cipher import AES #la fonction principale de cryptage , la documentation peut être trouvé sur pypi
import json #la fonction qui va nous permettre de mettre les données sur un format plus accessible
from base64 import b64encode ,b64decode#la fonction base64 qui va nous permettre de chiffrer
from Cryptodome.Util.Padding import pad,unpad
from argon2 import PasswordHasher, exceptions
import zlib
import base64
import random
import string

"""
    the technic that we gonna use to generate the key is as follow
    we compress the resulted hash using zlib
    we encode the resulted stream using base64
    we select 16 random characters from the resulted string 
"""

def generate_key(string):

    compressed_string = zlib.compress(bytes(string,'utf-8'),level=4) #we compressed the string using zlib
    encoded_string = base64.b64encode(compressed_string).decode() #we compute the base64 and generate the result as a string
    generated_key = "".join(random.sample(list(encoded_string),32)) #we select 16 random character from the generated base64 as the key for our AES encryption
    return generated_key


"""
la fonction qui permet de chiffrer prend un seule argument le mot de pass la clé est definit par default
la fonction est implementé avec AES 16 bites de clé
"""

def password_encode(password,key):

    data =bytes(password,encoding='UTF-8') #aes ne fonctionne qu'avec les bytes donc il faudra transformer tous en bytes 

    key=bytes(key,encoding='UTF-8') #on definit une clé qui a 128 bits pour rendre le cryptage plus compliqué


    cipher = AES.new(key,AES.MODE_CBC) #on utilise le mode cbc pour chiffrer

    cipher_bytes = cipher.encrypt(pad(data,AES.block_size)) #on utilise la fonction pad pour generer les paddings

    initial_vector = b64encode(cipher.iv).decode('utf-8') #on encode le vecteur initial en base64

    password = b64encode(cipher_bytes).decode('utf-8') #on encode le mot de passe chiffré en base64

    resultat = json.dumps({'initial_vector':initial_vector, 'password':password})

    return resultat


def password_decode(data,key): #le conseil c'est de passer les données à cette fonction sous forme de dictionnaire

    #si les données viennent en json il faudra les décodés avec la fonction json.load(data)
    #si c'est un dictionnare tout le monde sait comment obtenir les données 

    try:
        
        key = bytes(key,"utf-8")

        password_base64 = b64decode(data["password"]) #on prend le mot de passe 

        password_vector = b64decode(data["initial_vector"]) #on prend le vecteur initial

        cipher = AES.new(key,AES.MODE_CBC,password_vector) #on appel la fonction aes pour qu'lle initialise ses fonctions

        password = unpad(cipher.decrypt(password_base64),AES.block_size).decode('utf8') #on decode le message en enlevant les paddings
    
    except Exception as e:
       #on capture l'erreur et on l'affiche
        return e

    return password

#la fonction utf8 nous permet d'avoir le message en string

class PasswordManager:
    def __init__(self):
        # Create a PasswordHasher object
        self.hasher = PasswordHasher(hash_len=64,salt_len=8)

    def encrypt(self, password):
        # Generate a random salt

        # Encrypt the password using the salt and return the resulting hash
        return self.hasher.hash(password)

    def verify(self, password, hash):
        # Check if the password matches the given hash
        try:
            self.hasher.verify(hash, password)
            return True
        except exceptions.VerifyMismatchError:
            return False

def generate_pass(lenght):

    return ''.join(random.sample(list(string.ascii_letters*(lenght*3) + string.digits*lenght + string.punctuation*lenght),lenght))
    