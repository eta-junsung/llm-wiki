# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

---

## [2026-05-21] ingest | RX_control PWM 개발 가이드

- 소스: `projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md` (2026-04-14 작성, `01_RX_control` 서브시스템)
- raw 복사본: `teams/c/oled_tv_software/raw/RX_control_PWM_가이드.md`
- 생성 페이지:
  - sources: [[rx_control_pwm_가이드]]
  - entities: [[rx_control]], [[tim8]], [[tim3]]
  - concepts: [[pwm_system]], [[dead_time]], [[trip_zone]], [[uart_command_set]]
- 핵심 합의: TIM3에 BDTR이 없어 시스템 전체가 SW CCR offset 방식 dead time으로 통일됨. `pwm_set_freq()` 후 ARR이 바뀌므로 `pwm_set_deadtime()` 재호출 필요.
