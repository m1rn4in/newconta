# ContaBot

A bot built with GPT-3.5 and Python, connected to Ms Teams. It is specialized in responding to questions about accounting in Pacifico.

# Architecture

## Internal Architecture

For more details about this architecture, please see the `docs/readmes/bot-internal-architecture.md` file.

## External Architecture

For more details about this architecture, please see the `docs/readmes/bot-external-architecture.md` file.

# Usage

## Requirements
- **ngrok** to expose a local port to the internet.
- **docker** to quickly set up the project.
- **Azure Bot** - An Azure bot service, using the Inetum Azure account.
- Request a new application in Ms Teams, using the new Azure Bot application ID and the new bot icon.

## Installation
- Clone the repository
```bash
git clone git@github.com:pacificodesarrollogithub/ContaBot.git
```
- Build the project image.

```bash
docker build -t botpacifico_image .
```
- Run the project

```bash
docker-compose up -d && docker-compose logs -f ContaBot

```

- without docker:


```
source venv/bin/activate
sudo apt update -y
sudo apt install pip -y
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

## Connect the bot with Teams

- Run **ngrok**

```bash
ngrok http 8001 --host-header="localhost:8001"
```

```bash
docker-compose exec ContaBot bash

jupyter notebook --allow-root --ip=0.0.0.0 --port=8080

```
run save1.ipynb

- Set the **ngrok** host in **Azure Bot**. For more information, review [video](https://www.youtube.com/watch?v=oirW1hba-q8&list=PLSxMh3dfmJ0fX1X14tHfVhlEcU8e4C1dS&index=1&ab_channel=SoftTouch)

## Next Steps
- Improve the data from the Excel file.

- Encrypt user messages before generating responses.

- Filter the last 5 messages per user, using the metadata sent by Ms Teams along with the message.

- Scale the project.
- new developmet

