-- insere moeda, comeca e joga (anda para a direita e aperta os botoes) tirando capturas
local ports = manager.machine.ioport.ports
local function f(tag, name) return ports[tag].fields[name] end
local coin, start = f(":IN0","Coin 1"), f(":IN0","1 Player Start")
local right, b1, b2, b3 = f(":IN0","P1 Right"), f(":IN0","P1 Button 1"), f(":IN0","P1 Button 2"), f(":IN0","P1 Button 3")
local up, down = f(":IN0","P1 Up"), f(":IN0","P1 Down")
local frame, n = 0, 0
local EVERY = tonumber(os.getenv("EVERY") or "100")
local MAXF = tonumber(os.getenv("MAXF") or "14000")
emu.register_frame_done(function()
  frame = frame + 1
  local function press(fld, from, len) if frame >= from and frame < from + len then fld:set_value(1) end end
  coin:set_value(0); start:set_value(0); right:set_value(0); b1:set_value(0); b2:set_value(0); b3:set_value(0); up:set_value(0); down:set_value(0)
  press(coin, 700, 4); press(coin, 740, 4)
  if frame >= 1900 and frame % 200 < 12 then start:set_value(1) end
  if frame > 2100 then
    -- escolher personagem / avancar textos: botao 1 a cada 20 quadros; depois joga
    if frame % 24 < 3 then b1:set_value(1) end
    if frame > 2600 then
      right:set_value(((frame // 90) % 4 ~= 3) and 1 or 0)
      if frame % 60 < 3 then b2:set_value(1) end
      if frame % 300 < 3 then b3:set_value(1) end
      if (frame // 200) % 2 == 0 then up:set_value(frame % 50 < 20 and 1 or 0) else down:set_value(frame % 50 < 20 and 1 or 0) end
    end
  end
  if frame % EVERY == 0 then manager.machine.video:snapshot() end
  if frame >= MAXF then manager.machine:exit() end
end)
