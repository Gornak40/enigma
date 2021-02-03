#!/usr/bin/python3
import click
import rsa
import pickle


@click.group(help='Enigma - simple tool for cryptography using RSA algorithm.')
def enigma():
	pass


@enigma.command(help='Generate public and private keys.')
@click.option('--publ', '--public', type=click.Path(dir_okay=False, writable=True), help='Path to public key file.', default='public')
@click.option('--priv', '--private', type=click.Path(dir_okay=False, writable=True), help='Path to private key file.', default='private')
@click.option('--bits', type=int, help='Number of bits in keys.', default=512)
def gen_keys(publ, priv, bits):
	with open(publ, 'wb') as publ_file, open(priv, 'wb') as priv_file:
		publ_key, priv_key = rsa.newkeys(bits)
		pickle.dump(publ_key, publ_file)
		pickle.dump(priv_key, priv_file)


@enigma.command(help='Print public and private keys.')
@click.option('--publ', '--public', type=click.Path(exists=True, dir_okay=False, readable=True), help='Path to public key file.', default='public')
@click.option('--priv', '--private', type=click.Path(exists=True, dir_okay=False, readable=True), help='Path to private key file.', default='private')
def show_keys(publ, priv):
	with open(publ, 'rb') as publ_file, open(priv, 'rb') as priv_file:
		publ_key = pickle.load(publ_file)
		priv_key = pickle.load(priv_file)
		print(publ_key)
		print(priv_key)


@enigma.command(help='Encrypt file.')
@click.argument('file', type=click.File('rb'))
@click.argument('out', type=click.File('wb'))
@click.option('--publ', '--public', type=click.Path(exists=True, dir_okay=False, readable=True), help='Path to public key file.', default='public')
def encrypt(publ, file, out):
	with open(publ, 'rb') as publ_file:
		publ_key = pickle.load(publ_file)
		data = file.read()
		crypted = rsa.encrypt(data, publ_key)
		out.write(crypted)


@enigma.command(help='Decrypt file.')
@click.argument('file', type=click.File('rb'))
@click.argument('out', type=click.File('wb'))
@click.option('--priv', '--private', type=click.Path(exists=True, dir_okay=False, readable=True), help='Path to private key file.', default='private')
def decrypt(priv, file, out):
	with open(priv, 'rb') as priv_file:
		priv_key = pickle.load(priv_file)
		crypted = file.read()
		data = rsa.decrypt(crypted, priv_key)
		out.write(data)


if __name__ == '__main__':
	enigma()