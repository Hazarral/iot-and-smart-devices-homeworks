Cloud terminal:
```
[2026-05-11T12:50:01.011Z] Received LUIS prediction payload.
[2026-05-11T12:50:01.015Z] Intent 'CancelTimer' validated. Sending Direct Method to IoT Device...
[2026-05-11T12:50:01.102Z] Command dispatched. Device responded with status: 200
[2026-05-11T12:50:01.105Z] Executed 'TimerHttpTrigger' (Succeeded, Id=f9c8b7a6, Duration=94ms)
```

Hardware terminal (virtual device):
```
[DEVICE] Booting Virtual IoT Timer...
[DEVICE] Connected to Azure IoT Hub. Listening for commands...

[DEVICE] ⏱️ Timer started for 30 seconds...
   ... 30 seconds remaining
   ... 29 seconds remaining
   ... 28 seconds remaining

[DEVICE] 🔴 Received 'cancel_timer' command from Azure Cloud.
[DEVICE] 🛑 Timer successfully aborted by user command.
[DEVICE] ⏹️ Timer thread terminated early.
```