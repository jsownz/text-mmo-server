#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

HOST = ''
PORT = 34000
BUFSIZ = 1024
ADDR = (HOST,PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_incoming_connections():
  while True:
    client, client_address = SERVER.accept()
    print("%s:%s has connected." % client_address)
    client.send(bytes("Welcome to the server! What's your name?", "utf8"))
    addresses[client] = client_address
    Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
  name = client.recv(BUFSIZ).decode("utf8")
  welcome = 'Welcome %s, type {exit} to exit.' % name
  client.send(bytes(welcome, "utf8"))
  msg = "%s has joined the server!" % name
  broadcast(bytes(msg, "utf8"))
  clients[client] = name
  while True:
    msg = client.recv(BUFSIZ)
    if msg != bytes("{exit}", "utf8"):
      broadcast(msg, name+": ")
    else:
      client.send(bytes("{exit}", "utf8"))
      client.close()
      del clients[client]
      broadcast(bytes("%s has left the server." % name, "utf8"))
      break

def broadcast(msg, prefix=""):
  for sock in clients:
    sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
  SERVER.listen(10)
  print("Accepting connections...")
  ACCEPT_THREAD = Thread(target=accept_incoming_connections)
  ACCEPT_THREAD.start()
  ACCEPT_THREAD.join()
  SERVER.close()