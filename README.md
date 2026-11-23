# Custom Admin Logs Bot

## Wymagane
- Python 3.10+
- Bot Discord z włączonym Server Members Intent i Message Content Intent
- Bot na serwerze z uprawnieniami View Audit Log, Send Messages, Embed Links

## Konfiguracja (sekrety środowiskowe)
Ustaw `DISCORD_TOKEN` (token bota) oraz `LOG_CHANNEL_ID` (ID kanału logów).
Nigdy nie wklejaj tokena do publicznego repozytorium ani na czat.

## Uruchomienie
```bash
python -m pip install -r requirements.txt
python bot.py
```

Uwaga: Discord nie zawsze udostępnia pewne szczegóły zdarzeń; identyfikacja osoby wykonującej akcję
w przypadku usunięć wiadomości i wyjść członków może wymagać odczytu Audit Log i dopasowania wpisów.
Ten starter loguje zdarzenia, ale nie gwarantuje pełnego wskazania sprawcy w każdym przypadku.
