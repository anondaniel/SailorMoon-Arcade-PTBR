-- tira uma captura a cada N frames para ver as telas do modo demonstracao
local out = "C:/Projetos/15_Pretty_Soldier_Sailor_Moon_Arcade/04_Graficos/capturas/"
local frame, n = 0, 0
local every = 180
emu.register_frame_done(function()
  frame = frame + 1
  if frame % every == 0 then
    n = n + 1
    manager.machine.video:snapshot()
    if n >= 120 then manager.machine:exit() end
  end
end)
