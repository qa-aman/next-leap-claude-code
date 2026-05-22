# RecordingControls

Top toolbar during the live meeting. Recording indicator + timer on the left, call controls on the right.

## Anatomy
- Left: red "Recording" pill (pulsing dot) + monospace timer (mm:ss, ticking)
- Right: Unmute/Mute (danger when muted), Share screen, Participants count, End meeting (danger)

## Behavior
- Timer ticks every second from a demo starting value (02:34) so the prototype feels alive on first paint
- Mute toggles between primary-danger ("Unmute") and secondary ("Mute") variants

## Mirrored from
- `screenshots/dialpad-01.png` - bottom toolbar pattern adapted to the top of the layout for visibility.
- `screenshots/otterai-03.png` - Stop Notetaker pill + REC timer indicator.

## Props
- `onEnd: () => void` - typically navigates to /summary
