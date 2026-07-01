# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

---

## [2026-07-01] 환원 | 전사 펌웨어 컨벤션 skill(eta-firmware-conventions) 플러그인 배포 기록

- 정본 [[firmware_naming_conventions]]·[[firmware_layering]]에서 추출한 Claude skill **`eta-firmware-conventions`**를 플러그인으로 배포(`eta/eta-ai-tools/eta-firmware-conventions`: `.claude-plugin/plugin.json` + `skills/eta-firmware-conventions/{SKILL.md, references/naming.md, references/layering.md}`). 네이밍 + BSP/HAL/ALG/App 배치를 작성·리뷰 양방향으로 안내. 범위 제외 = git workflow.
- **갱신**: [[firmware_naming_conventions]] — 종전 "추후 skill 승급 예정" → **배포 완료**로 정정 + 배포 노트. [[firmware_layering]] — 배포 노트 신설. [[index]] — 두 항목에 skill 배포 clause.
- **동기화 규약**: 위키 두 페이지가 정본 단일 소스, skill은 추출본(정본→skill 단방향 재동기화).
- ⚠️ lint: SKILL.md "출처" 경로가 타 머신 기준(`/Users/jun/eta/wiki/...`) — 재동기화 시 실제 경로 확인 필요.

## [2026-07-01] ingest | g팀 8kw Io 2차 IIR 저역통과 필터(io_iir_lpf) 스펙 수령

- 미팅 결과: **Io ADC 스위칭 노이즈 제거용 2차 IIR biquad 저역통과 필터** 구현 결정. 설계자 스펙 3종 수령.
- **원본 복사**(raw, first-ingest-wins): `raw/io_iir_lpf/io_iir_lpf_spec.html`(계수·차분식·코드매핑) · `io_iir_lpf_sim.xlsx`(Excel 시뮬) · `digital_filter_impl_16bit_micros.pdf`(고정소수점 구현 일반 참고). ⚠️ `digital_filter_chart.png` 미수령(HTML 차트 깨짐).
- **신설**: [[io_iir_lpf]] (source 페이지 — Direct Form I 2차 biquad LP. 차분식 `out0=b0·in0+b1·in1+b2·in2+a1·out1+a2·out2`, a1/a2 부호 접힘=더함. 85kHz 코드계수 b0=b2=9.75e-6·b1=1.95e-5·a1=1.987473·a2=−0.987512, Excel 40kHz값 구분. 입력 `−Vadc/2` 바이폴라 보정. ALG biquad+App 배치, R5F FPU→float, C2000/CLA 포팅. §6 착수전 확정 4건).
- **갱신**: [[status]] — deferred→활성 트랙 승격(다음 시작점="io_iir_lpf 구현만 먼저 → ADC 안정화"), 구현 현황표 행 추가. [[index]] — Sources 행 추가.
- **범위 결정**: 필터는 **구현만 먼저**, 실보드 검증은 ADC 안정화([[fod_i_coil_observation]]·[[adc_noise_fft_probe]]) **이후**. A5(리피터 버스트 N=16)·A6(SW 이동평균)와 직교(재귀형 IIR LPF).
- **미확정(추론 금지)**: "Io"=어느 채널(I_COIL_SEN 추정)·`−Vadc/2` 바이폴라 보정 적용 여부(단극성 DC 포락선 가능성)·신호체인 삽입 위치·A6 대체/보완 여부.
- 작업 세션 전달 프롬프트 작성 완료.

## [2026-07-01] ingest | c팀 oled_tv_software 펌웨어 레이어링 재구성 세션 환원

전사 표준([[firmware_layering]]·[[firmware_naming_conventions]]) 기준으로 02_rx_esb·03_tx_esb·04_tx_control 4레이어 재구성 진행 세션의 지식 환원. 변경 4범주:

**(A) 드리프트 정정** (코드 기준 사실 반영):
- `nrf52_module_naming`: 03_TX_ble eta_* 전환 상태 이미 정정됨(2026-06-30 선반영)
- `status.md`·`roadmaps/04-tx-control-dummy.md`: 04 `.ioc` 파일명 `TX_control.ioc` 개명 완료로 정정(N1 확인)
- `cubeide_cli_build_trap`: CubeMX 재생성 금지 근거에 04 `.ioc` 내용 불일치 사례 보강
- `CLAUDE.md`: 04_TX_control 서브프로젝트 추가, 01/02/03→01/02/03/04
- `app_protocol_module`: `_shared` "세 펌웨어 공유"→"네 펌웨어 공유", `pkt_print_*` 소비처 02/03→02/03/04, 섹션 타이틀 3→4펌웨어

**(B) 표준·개념** (이번 세션 확정 결정·발견):
- `firmware_naming_conventions` §1: `comm_st` 약어 화이트리스트 등재
- `app_protocol_module`: App 모듈 역할 네이밍 원칙 신설 — relay(02/03·중계) vs protocol(01/04·종단점)
- `nrf52_firmware_conventions`: nRF52 BSP/HAL 레이어 경계 원칙 신설 — SDK 드라이버 핸들 단위로 HAL에 묶는 이유
- `ses_build_conventions` §5: `BOARD_CUSTOM`/`custom_board.h` 기계 신설 — 핀 공급 경로·컴파일아웃 메커니즘·BSP 통합 후보
- `firmware_layering` §6: c팀 적용 현황표 갱신 — 02 4레이어 전환 진행중(SES 빌드 통과·실보드 검증 대기), 03/04 대기

**(C) `_shared` 분할 특성화**: `spi-esb-refactor` §7 신설 — 5개 책임 분류(wire 계약/ALG/printf/보드핀/정책상수)·누수 2건·우산-shim 계획

**(D) status·roadmap 갱신**: `status.md` 레이어링 재구성 표 신설(02 진행중·_shared/03/04 미착수). `roadmap.md` §5 레이어링 환원 항목 추가.

## [2026-07-01] 결정 | 8kw ADC A4 실행 순서 확정 — A5·A6 뒤로 배치

근거: 사용자 결정 — A4(실보드 교차검증)를 로드맵 실행 순서상 A5·A6 뒤로 명시. A5(리피터 버스트/필터)가 ADC 출력 특성을 바꾸므로 정확도 교차검증은 안정화 후에 해야 유효(종전 "[추정] 독립·확인 필요" 해소).

- **실행 순서 확정**: A5 필터 안정화(FOD 노이즈 측정→최종 N/위상) → A6 SW 이동평균 → A4 실보드 교차검증 → (PWM P4 제어루프).
- **[[adc]]**: §1 마일스톤 표 제목 A0~A4→A0~A6, A4 행에 "실행은 A5·A6 뒤" 명기, 표 아래 "실행 순서 ≠ 번호 순서" 노트 추가. §A5 표 "A4 선후 관계" 확인필요→확정. §남은 절차에 A4 마무리 추가. §3 현재 위치 "다음" 순서 반영.
- **[[roadmap]]**: adc 행 "다음" 포인터를 A5→A6→A4 순서로 교체.
- **[[status]]**: 다음 작업 제목·A3.5 잔여·A5 항목·A4 미결·구현현황 표를 A5·A6 후 A4 순서로 정합.

## [2026-07-01] 결정 | 8kw PWM P3 보호(trip-zone) 마일스톤 드롭 (프로젝트 전체)

근거: 사용자 결정 — PWM P3 보호(trip-zone)는 아예 뺄 수 있는 작업. 과전류·과전압 보호는 HW 비교기(TLV3231+SN74HCS21 인터록→GD_EN)가 담당하므로 펌웨어 trip-zone 불요. living-doc 전체에서 제거, 과거 주간보고 2건(스냅샷)은 보존.

- **PWM 로드맵 호 재구성**: `roadmaps/pwm.md` 마일스톤 표에서 P3 행·P3 섹션·"보호(trip) 신호 소스" 블로커 삭제. 호 표기 `P0~P4`→**`P0~P2·P4`**(P4=제어루프 유지, 번호 재배열은 cross-doc 리스크로 미실시 — P3 슬롯만 비움). 기본 출력→dead-time→ADC 제어 순으로 정정.
- **living-doc 전파 제거**: [[roadmap]](pwm 행·현재위치 2곳)·[[status]](다음작업 제목·활성트랙·구현현황·P0~P4 라벨)·[[team_briefing_8kw]](ASCII 호·보고포인트·현황)·[[firmware_layering_8kw]](eta_alg_control 진입조건 P3→P4)·[[pwm_pinmap]](trip 신호 소스 P0잔여)·index.md(pwm 카탈로그). 모든 "다음=P3 보호" 포인터를 실제 다음(dead-time 최종값/게이트 극성 회로도/P4 제어루프)으로 교체.
- **보존**: [[board_schematic_v1_0e00]]의 HW 보호신호(비교기→GD_EN 인터록)는 회로도 사실이라 유지. [[status]] §repeater 미채택 근거의 "과전류·과전압 보호=HW 비교기" 서술도 ADC 설계 근거라 유지. 과거 주간보고 2건 불변.
- **GPIO95 잠복충돌 노트**: 사용자 결정으로 주간보고에서만 제거, living-doc([[status]]·[[fod_i_coil_observation]]·[[adc_noise_fft_probe]])엔 다음 FOD 작업 주의사항으로 유지.

## [2026-07-01] 결정 | 8kw FOD 실행순서 확정 — 안정화 선행

근거: 사용자 결정 — 다음 작업 순서를 ① I_COIL_SEN 노이즈 측정 → ② N/위상 튜닝 안정화 → ③ 안정화 후 FOD(이물) 변화 관찰로 확정. FOD 문서의 "정상·이물 동시캡처 후 필요시 안정화" 흐름을 σ 선감소로 재배열(Δ/σ 유리 + 튜닝을 이물 변수 없이 수행).

- 갱신 [[status]] 다음 시작점(3단계 안정화-선행 순서), [[fod_i_coil_observation]] §3(채택 실행순서 노트), [[weekly_report_2026-06-24_30]] 다음 작업.

## [2026-07-01] 환원 | 8kw FOD — I_COIL_SEN 단독 백색/상관 판별 타당성 근거

근거: 사용자 질의 — 정상 상황에서 I_COIL_SEN에만 프로브를 두고 백색 vs 스위칭 상관을 판별해도 되는 이유. [[fod_i_coil_observation]] §1에 근거 4항 환원.

- **[[fod_i_coil_observation]] §1 "왜 I_COIL_SEN 단독 판별이 타당한가" 신설**: ① 이기려는 σ가 곧 I_COIL_SEN 노이즈(직접성) ② 정상상태 공칭 DC → FFT 대역 AC=노이즈(GA_Vin과 동일 성질) ③ 백색/상관 이분법이 노드 무관하게 치료법 직결 ④ **정류 리플 단서가 결정을 못 뒤집음** — 리플·결합노이즈 둘 다 coherent+위상고정 → 같은 레버(위상) 요구 → 결정 트리 강건. 경계: "GA_Vin 더 깨끗"은 절대 플로어 정밀측정 얘기일 뿐. 실무: 마커 GPIO95가 이미 I_COIL_SEN에 걸려 coherent 관측.

## [2026-07-01] 환원 | 8kw-ev-wpt-tx FOD I_COIL_SEN 1차 관찰 절차 (다음 작업)

근거: 코드 repo `docs/fod_i_coil_observation.md`(branch `feature/adc-noise-fft`) 환원 — 다음 이어서 할 작업. 회로도 [[board_schematic_v1_0e00]] line 43 신호체인과 대조.

- **신설 [[fod_i_coil_observation]]** (8kw concept): FOD 1차 관찰 절차·결정 로직. ① 신호체인 — I_COIL_SEN(J3.28)=CT(T1 7mV/A)→CR3~6 쇼트키 정류→R30~32+C55 2.2µF RC평활된 **DC 포락선**(이물→코일전류 변화→DC 레벨 시프트=FOD 신호) ② 2트랙 셋업(스코프 DC/AC/FFT/시간축 + GUI 10Hz ch4 CSV) ③ 절차·검출성 `Δ(이물)/σ(정상노이즈)` ④ 센싱 안정화(백색→N↑ / 상관→위상, [[adc_noise_fft_probe]] 공유) ⑤ 풀레이트 디지털(온타깃 버스트 캡처+UART 덤프)은 미룸.
- **★ stale 정정 [[adc_noise_fft_probe]] §2**: I_COIL_SEN(J3.28) "85 kHz 신호 자체라 FFT 부적합" → **정류·평활 DC 포락선**으로 정정. CT 1차측이 85 kHz일 뿐 ADC 핀은 DC. 순수 노이즈 플로어엔 GA_Vin/GA_Iin이 더 깨끗(정류 리플 상재)하나 **FOD 프로브로는 J3.28이 정본**. 마커 노트에 브랜치·[[fod_i_coil_observation]] cross-ref 추가.
- **갱신 [[status]]**: 다음 시작점을 FOD 1차 관찰(branch `feature/adc-noise-fft`)로 교체 — 2트랙 캡처·Δ/σ·신호체인 정정·OC 제약. FOD 병행 트랙 노트를 마커 잠복충돌 노트로 슬림화. date 2026-07-01.
- **갱신 [[weekly_report_2026-06-24_30]]**: 다음 작업 §를 FOD 1차 관찰 중심으로 재구성.
- 갱신 index.md(FOD 엔트리 + adc_noise_fft_probe I_COIL 서술 정정).

## [2026-07-01] 작성 | 8kw-ev-wpt-tx 주간 업무 보고 2026-06-24~30 신설

근거: 저번 업무보고(6/24, 기간 6/17~23) 이후 일주일 작업 정리. status·log·roadmap(adc)·주간보고 커밋 기록 종합.

- **신설 `weekly_report_2026-06-24_30.md`**: ① 6/24 확정 작업 처리(GUI 소수점 3자리·트리거 전환+HW평균 완료) ② ADC 트리거 RTI→EPWM0_SOCA + PPB N=64(PR #6) ③ PPB 누적→리피터 버스트 블록평균 N=16 전환(PR #11, 출력 85kHz 복귀) + Saleae 실측(85.03kHz·트리거당 OSINT 1회) + 변환예산 N상한~41 ④ 8kW 회로도 센서 신호체인 분석 + FFT 측정계획 ⑤ FOD 1차 관찰 착수(`6993a40`). (개발환경 정리·화면 녹화·전사 표준화 항목은 사용자 요청으로 제외)
- 갱신: index.md 주간보고 엔트리 추가.

## [2026-06-30] 환원 | 8kw ADC N=16 리피터 버스트 타이밍 — Saleae 실측 인입

근거: Saleae Logic2 디지털 캡처(ch0=EPWM2_A·ch1=GPIO95 OSINT ISR, 12,260주기, ≈144 ms). 코드 트리 `6993a40`에서 file:line 전건 재확인(`eta_bsp_adc.c`:60/156/160/172/196–230, `eta_bsp_adc.h`:31, `ti_drivers_open_close.c`:373/491/494/539/542, `example.syscfg`:202/224–231, `adc/v2/adc.h` sampleWindow≥16→ACQPS=15). 신규 source 페이지 + raw 증거 보관 + 플랫폼 3페이지 환원.

- **신규 [[adc_repeater_burst_timing]]** (8kw source) + 원본 CSV `raw/adc_repeater_burst_timing/digital.csv`(764K) 보관. 측정(사실)/역산(추론 상한) 라벨 분리.
- **사실 (측정)**: 트리거당 OSINT 정확히 1회=85.03 kHz(12,260/12,260, 누락·중복 0)→**리피터 버스트 실증**(분산 누적이면 ≈5.3 kHz여야 함). 트리거(EPWM0 ZERO)→버스트끝(ISR 진입)=3.12 µs(주기 26.5%), ISR 0.304 µs, EPWM2_A 상승→GPIO95 상승≈동시(+5 ns).
- **추론 (상한)**: 실효 cadence ≤195 ns/변환(IRQ 진입지연 포함 상한)<정적 285 ns. ADC1(32변환) ~53% [추론, 미측정].
- **★ stale 정정**: [[am263p_adc_instance_allocation]] "현 채택=PPB 누적/8kw N=64(LOG2=6)" → **리피터 버스트 N=16(LOG2=4) 실채택**으로 정정(측정이 실증). 정적 285 ns/N≤41 모델은 보수 상한으로 병기 유지.
- **빈자리 충족**: [[am263p_adc_ppb_averaging]] §6 "트리거당 N회=OSINT 레이트 동시 확인" 충족(ADC0). [[am263p_adc_instance_allocation]] "라이브 실측 미수행"→1차 인입.
- **미확정 유지(봉합 안 함)**: IRQ 진입지연 분해·레지스터 필드 readback(NSEL/LIMIT/SHIFT/COUNT)·ADC1 OSINT 횟수·마지막변환 마감공식.
- **방법론 메모**: 1차 판독 "E2 상승→G95 상승 6.284 µs"는 하강엣지 기준 착오(E2 하강→G95 상승=6.285 µs로 재현). 향후 기준 엣지 확인.
- 갱신: [[am263p_adc_repeater_burst]] §3·§6, [[am263p_adc_instance_allocation]] 변환예산·빈자리, [[am263p_adc_ppb_averaging]] §6·§5·§7·§8, index.md, 세 페이지 frontmatter date.

## [2026-06-30] 환원 | 8kw "ADC 필터 전환"(2026-06-29) 핸드오프 — stale 교정 + 신규 커밋 반영

근거: 삭제된 branch `docs/adc-filter-handoff`/handoff.md(2026-06-29 스냅샷) 전문 + 현재 코드(`src/bsp/eta_bsp_adc.{c,h}`, `example.syscfg`) 대조. 핸드오프 발견 ①~⑥(직교성·SAR 합예산 비대칭·N=64≠리피터기각·채널배치·이중경로·어긋남)은 **PR#11 머지 후속 환원(`d41a5ce`)에서 이미 플랫폼 페이지에 반영**됨([[am263p_adc_repeater_burst]]·[[am263p_adc_instance_allocation]]) — 중복 환원 안 함. 이번엔 **stale 교정 + 미반영 신규 커밋**만.

- **stale 교정 (branch→main)**: 8kw 전술 페이지([[status]]·[[adc]] §A5)가 리피터 버스트를 "branch `feature/adc-repeater-burst`/main 미머지/main은 N=64"로 적고 있었음 → 실제는 **PR#11 squash 머지 main `2c4ff85`(CI pass), 현 운영 N=16**(`ETA_ADC_OVERSAMPLE_LOG2=4U`). 코드·플랫폼 페이지와 정합화.
- **OSINT 레이트 어긋남⑥(a) 해소**: 버스트 전환으로 출력=85 kHz/인스턴스 복귀 → N=64 누적기 수치 "1.33 kHz"(및 코드 주석 "2.66 kHz")는 더 이상 적용 안 됨 명시(라이브 재실측 권장).
- **신규 커밋 `6993a40` 반영** (핸드오프 이후): EOC ISR이 GPIO95(J4.31, 스코프 CH4) 토글로 샘플링-종료 마커, `ETA_BSP_ADC_DBG_MARK_IDX`로 인스턴스 선택(현재 `0U`=I_COIL_SEN/FOD 1차 관찰, `docs/fod_i_coil_observation.md`). ⚠️ `eta_hal_gpio` DBG_LOOP=GPIO95 잠복 충돌(후속 정리). → [[adc_noise_fft_probe]] §마커에 "구현됨"으로 반영(노이즈측정은 idx `3U`=GA_Vin), [[status]]에 FOD 병행 트랙 추가.
- **트리거 위상(D) 명문화**: 현 EPWM0_SOCA = `EPWM_SOC_TBCTR_ZERO`(syscfg 확인) → 스위칭 상관 시 위상이 레버. [[adc]] §A5 표 + [[adc_noise_fft_probe]].
- 갱신: [[status]](다음 시작점·A5 진척·구현현황·date), [[adc]](§A5 표·완료기준·date), [[adc_noise_fft_probe]](마커 구현).

## [2026-06-30] ingest | 펌웨어 4레이어 아키텍처 전사 표준 승급

근거: 사용자 결정 — g-8kw 4레이어(BSP/HAL/ALG/App)를 전사 아키텍처 표준으로 승급. 네이밍 표준 승급과 동일 패턴([[firmware_git_workflow]] 표준 + walkthrough 실습 선례). 레이어링 ≠ 네이밍(직교: 아키텍처 vs 식별자)이지만 결정2 한 군데서 접점.

- **신설 [[firmware_layering]]** (루트 concept, 전사 공통): g-8kw de-facto를 플랫폼 무관하게 일반화. 레이어 정의(BSP/HAL/ALG/App 책임·의존)·**불변식 하드룰**(R1 ALG는 HW 모름·R2 의존 단방향·R3 SDK는 HAL/BSP 안에만)·§3 배치규칙("PC서 도나?" 리트머스)·**§4 4개 강제 아님**(ALG 비어도·BSP+HAL 병합 2레이어도 준수, 불변식만)·§5 네이밍 연결(→ [[firmware_naming_conventions]] §4)·**§6 팀적용**(g-8kw 풀4레이어=레퍼런스 / c-nRF52 app+driver 2층 [[nrf52_firmware_conventions]] / c-STM32 부분 [[app_protocol_module]]).
- **리네임 [[firmware_layering_8kw]]** (← `firmware_layering.md`, `git mv`): g-8kw 구체 적용으로 슬림화 — 모듈 인스턴스·빈 경계(eta_alg_control·eta_hal_pwm A3/P3 대기)·gui.py:74 결합·PR #5 검증만 잔류. 레이어 모델은 표준 위임.
- **백링크 분기**: 개념/표준 참조(naming 페이지 3곳)는 `[[firmware_layering]]`, 프로젝트 구체 참조(status·roadmap·pc_monitor_gui·index g-8kw)는 `[[firmware_layering_8kw]]`. 역사 로그 2건은 lineage 주석 달아 `_8kw`로 교정.
- **갱신 index.md**: 루트 공통 Concepts에 표준 등록 + g-8kw 엔트리를 `_8kw`로 교체.

## [2026-06-30] ingest | 전사 펌웨어 네이밍 컨벤션 표준 수립

근거: 8kw-ev-wpt-tx 펌웨어 de-facto 네이밍 관행을 정본화하는 작업에서 **전사 공통 표준**으로 스코프 확대(추후 Claude skill 승급 전제). g-8kw `src/{bsp,hal,alg,app}/` de-facto를 grep 재확인 + **BARR-C:2018 / MISRA C:2012 / Linux kernel / Zephyr RTOS / SEI CERT DCL37-C를 웹 검증**해 산업 정합성 전면 재감사.

- **신설 [[firmware_naming_conventions]]** (루트 concept, 전사 공통): de-facto 16항목 재감사 — 대부분 BARR-C(MISRA 조화)와 정합 확인. **앵커 결정**: 사용자 ruling — 임박 인증 제품 없음 → **MISRA-필수 하드룰 + 현대 임베디드 하이브리드**(풀-BARR-C 아님, 순수 Linux 미니멀도 아님).
  - **핵심 교정**: MISRA ≠ BARR-C 헝가리안. 기능안전(IEC 61508·ISO 26262)이 인용하는 건 MISRA고, MISRA는 헝가리안 `g_`/`p_`/`b_`를 의무화 안 함(충돌·UB 방지 규칙뿐). `_t`는 오히려 MISRA가 *지적*(POSIX 예약). ⟹ `p_`/`b_` 미채택·`_t` 유지+편차문서화가 정답.
  - **하드룰**: 외부 31자 유일(5.1)·예약식별자/선행`_` 금지(21.x·C11 7.1.3)·stdlib/SDK 비충돌(7.1.b).
  - **편차원장**: D1 `_t`(DCL37-C/POSIX, 벤더생태계·`eta_` 충돌0)·D2 SDK 미개명·D3 루프변수 `i`/`j`(BARR-C 7.1.e 편차).
  - **결정1** 구조체 필드 snake + SDK 1:1 미러만 camel. **결정2**(§4 레이어 부록) 공개=모듈만/내부=레이어포함(gpio가 bsp·hal 양쪽 → 모호성 해소 + 31자 예산 복무).
  - **§6 팀수렴**: g de-facto=정본 · c-nRF52 `eta_` 이미 정렬 · c-STM32 PascalCase(Monitor_Loop) grandfather(신규부터 적용) · 전향노트(GA→IEC 61508/VA→ISO 26262, 제품별 qualified 분석기가 규칙셋 확정).
  - **제품 맥락**: eta WPT TX = GA(off-board 충전기) → IEC 61508 우산 / VA(차량측) → ISO 26262. SAE J2954 3파티션(GA/VA/BMS) 지도 인용.
- **갱신 [[firmware_layering_8kw]] §네이밍**: 전사 표준을 [[firmware_naming_conventions]]로 위임, 레이어드 한정 규칙(결정2)만 잔류. (당시 파일명 `firmware_layering`, 후속 세션에 표준 승격하며 `_8kw`로 리네임)
- **갱신 index.md**: 루트 공통 Concepts에 등록.

## [2026-06-30] ingest | 8kw 보드 회로도(Ver 1.0E00) + ADC 노이즈 FFT 프로브 결정

근거: 사용자 질의 — 다음 작업으로 스코프 FFT를 수행해 ADC 평균 N을 튜닝할지 트리거 위상을 조절할지 결정. 회로도가 wiki에 없어 ingest. 원본 `projects/g/8kw-ev-wpt-tx/docs/8kw_inverter_board_260506.pdf`.

- **원본 복사**: `teams/g/8kw-ev-wpt-tx/raw/8kw_inverter_board_260506.pdf` (first-ingest-wins — 다른 프로젝트는 [[board_schematic_v1_0e00]] 백링크).
- **신설 [[board_schematic_v1_0e00]]** (source): 6시트 ingest. 풀브리지 SiC 모듈 U6/U7(FF8MR12W1M1H)·게이트드라이버 U8/U9(FR20205VBDN)·DC링크 스너버. **ADC 센서 신호체인 표**(GA_Vin=U16 AMC0311 절연증폭기/DC버스, GA_Iin=U1 TMCS1126 Hall/입력DC전류, I_COIL=T1 PA6322 CT/85kHz 공진전류, Temp×2=모듈 NTC). MCU핀 입력 RC 100Ω+~1.33nF → **fc≈1.2MHz로 85kHz 미감쇠**. HW 보호 인터록(TLV3231 비교기+SN74HCS21/SN74LVC1G08→GD_EN). 접지 도메인(DGND=ADC 절연측 안전 / PRI_GND=HV 금지).
- **신설 [[adc_noise_fft_probe]]** (concept, 측정 전 계획): 결정 로직 정합 — 백색→N↑ / 스위칭 상관(85kHz 고조파)→트리거 위상. ★사용자 모델 보강 근거: ADC 트리거가 EPWM0_SOCA에 위상고정 → 스위칭 상관 노이즈는 매주기 coherent → √N 평균 무효 → 위상이 유일 레버(역으로 백색이면 위상 무의미·N만 유효). 프로브 포인트(GA_Vin J3.26·GA_Iin J3.29 DC핀 최적, I_COIL J3.28 부적합=85kHz가 신호), 타이밍 마커(HS1 J4.39 트리거 + 디버그 GPIO95 J4.31 OSINT 토글=샘플순간 마커), MSOX3104T 설정(Hanning·0~500kHz·RMS평균·짧은 GND), 결정 트리. 버스트 N=16=4.56µs≈주기 39% → 위상+저N 상호작용.
- **갱신 [[adc_pinmap]]**: source에 회로도 ingest 완료·센서 신호체인 cross-ref 추가, 백링크 2개.
- **갱신 index.md**: source·concept 2개 등록.

## [2026-06-29] 환원 | 8kw ADC 필터 전환 세션 — 리피터 버스트·EDMA·디버그 GPIO (B–F)

근거: 8kw-ev-wpt-tx ADC 필터 전환 세션 (2026-06-29, branch `feature/adc-repeater-burst`). 모든 SDK/TRM/UG 인용은 서브에이전트 3개로 file:line 교차검증 (헤더 결함·EDMA dma_xbar·GPIO P07 출처 포함).

- **신설 [[am263p_adc_repeater_burst]]** (lp-am263p 플랫폼): 트리거 리피터 오버샘플 버스트 SDK 사용법(`ADC_configureRepeater` adc.c:101–103, `ADC_RepeaterConfig` adc.h:797–802, `REPMODE_OVERSAMPLING=0x0`, `repCount=N−1`≤127, `TRIGGER_REPEATER1/2=0x7E/7F`, REPINST 2개/인스턴스 adc.h:773–774). ⚠️**SDK 헤더 결함**: `ADC_configureRepeater` 프로토타입이 adc.h에 없음 → 8kw 로컬 extern 우회(`eta_bsp_adc.c`:43–46). 누적 vs 버스트 대비·HW/SW 필터 직교성·버스트 N≤~41 예산.
- **신설 [[am263p_edma_adc_offload]]** (lp-am263p 플랫폼, 결정 보류): ADC→EDMA HW 근거(TDMAEN ch07_5:2120, 결과레지스터 복제 :2467, 64채널). ★빈자리 해소: TRM엔 ADC가 DMA 트리거 소스 표에 **없으나**(ch04 ADC DMA Requests 부재) **SDK가 ADC INT를 dma_xbar 소스로 제공**(`dma_xbar_am263px.syscfg.js`:69–93) → 가능. EDMA 실익은 ISR 폭증 회피·burst 원자전송 둘뿐(85 kHz 실적재 전제), 캐시는 비용. 미실증·보류.
- **신설 [[am263p_lp_debug_gpio]]** (lp-am263p 참조): J4 PR0_PRU0_GPIO0/1/2=GPIO93/94/95 Mode7(ug:1592–1594, pinmux.h:242–244), TS3DDR3812 1:2 mux(ug:911) + PRU_MUX_SEL=HIGH로 BP 헤더. ★P07/mask 0x80은 UG 본문 아닌 회로도+`eta_bsp_gpio.c`:44/47 근거. GPIO93=GD_EN 점유 → 디버그는 J4.31/GPIO95(commit `ef874d9`). 빈자리: J4.32(GPIO94) 헤더 무신호(회로도 미확인).
- **갱신 [[adc]] §A5/§A6**: A5 ✗→△ — PPB 누적(N=64) → 리피터 버스트 블록평균(N=16, 출력 85 kHz/인스턴스) 전환·실보드 검증(branch). 3단계 구현순(버스트✓→SW 이동평균 ISR write→EDMA 게이트), 검증 교훈("3채널 死"=일시 잔류, 펌웨어 결함 아님), 채널 재배치 권고.
- **갱신 [[status]]·[[roadmap]]**: 다음 시작점=리피터 버스트 노이즈 FFT→최종 N, 구현현황 A5 △, roadmap adc 호 A0~A6.
- **F 정정**: 변환 cadence 315→285 ns·N≤16~32→≤41(adc.md·index.md), `eta_bsp_adc.h:28`→`:31`, ppb_averaging에 버스트 짝 cross-ref. (텔레메트리 100 ms·N 런타임 우선은 기존 정정 유지.)

## [2026-06-29] 환원 | lp-am263p ADC 변환시간 예산 정밀 산정 (리피터 N 상한)

근거: AM263P ADC 리피터 N 상한 변환시간 정밀 산정 세션 (2026-06-29). TRM Table 7-123 + SDK adc.h/생성코드 인용 확인.

- **[[am263p_adc_instance_allocation]]** §"변환시간 예산"을 "변환시간 예산 & 리피터 N 상한"으로 갱신·정정:
  - 리피터 N 상한 모델 명시: Σ(SOC 리피트) × cadence ≤ 트리거 주기. 세 결정 인자(트리거 주기·1회 cadence·인스턴스 내 SOC 수).
  - 정밀값: tSH **80 ns**(ACQPS=15, sampleWindow 16−1) · tEOC **205 ns**(41 SYSCLK) · tLAT **220 ns**(44 SYSCLK), cadence ≈ **285 ns** → 주기당 ~**41 변환**, N 상한 ~41. (TRM :303/:2116-2118/:2171, `adc/v2/adc.h`:185·:888·:920, `ti_drivers_open_close.c`:134, `example.syscfg`:67)
  - **정정**: ① 종전 "ACQPS=16, window 85 ns" → **오인**(SDK가 sampleWindow−1 기록 → ACQPS=15, tSH=80 ns). 2026-06-26 로그의 "80→85 ns 보정"이 거꾸로였음. ② "conv 11.5 ADCCLK→230 ns" → Table 7-123 tEOC=205 ns가 정본. ③ "315 ns·~37 변환"은 과대(보수)치 — 틀린 게 아니라 보수적.
  - **리피터 N=64 기각 ≠ 리피터 기각** 명시: N=64는 64×285≈18.2 µs로 예산 초과 기각, 단 **N≤~41 저-N 리피터는 살아있는 선택지**(A5 후보).
  - 빈자리 호명: TRM 내부 불일치(:305 11.5 vs :2088 10.5 ADCCLK)·마지막 변환 마감 공식 미확정(N 1~2 깎임 가능)·데이터시트 최소 S+H 윈도우 미인입·전 항목 라이브 실측 미수행.
- **[[status]]** 갱신: repeater 미채택 근거 수치 285 ns로 정정, A5 샘플링 재작업에 N 상한·저-N 리피터 후보 반영.

## [2026-06-29] ingest | 8kw-ev-wpt-tx ADC 필터 전환 검토 세션 발견 환원

근거: ADC 필터 전환 검토 세션 (2026-06-29) — 6개 발견 환원.

- **roadmaps/adc.md** (8kw-ev-wpt-tx):
  - A1.5 텔레메트리 주기 "1초" → "100 ms / 10 Hz" 정정 (`example.syscfg`:245-249; commit 8b85bda 이후 변경).
  - A3.5 repeater 기각 범위 명시: N=64 한정. N≤~16~32는 예산 내, 저지연 선택지로 살아있음.
  - §A6 전면 재작성: HW 블록평균(PPB)↔SW 이동평균 직교성 원리표, 이중경로 설계(Fast Path→PID / Slow Path→OCP) 맥락, 파라미터 표.
- **am263p_adc_ppb_averaging.md** (lp-am263p):
  - §5 N 정본 주석 추가: SysConfig 주석 "32회"보다 런타임 `ETA_ADC_OVERSAMPLE_LOG2=6`(N=64)가 우선.
  - §5 ADC1 ISR 발화 횟수 빈자리 추가: OSINT2만 INT1 소스 — 배치당 ISR 1회 추정, OSINT1 별도 인터럽트 여부 실측 미수행.
- **am263p_adc_instance_allocation.md** (lp-am263p):
  - 리피터 예산 모델 보강: 인스턴스당 리피터 2개·NSEL 독립, 비대칭 분배 가능(합 예산 ~37 변환/주기), 변환시간 정적 산정 한계 명시.
  - repeater 기각 범위 정정: N=64 기각, N≤~16~32 유효.
  - 차기 PCB 채널 배치 권고 추가: TEMP×2 한 인스턴스, I_COIL/GA_Iin/GA_Vin 별도 인스턴스. 펌웨어-only 변경 불확실(AIN 핀 라우팅 의존).

## [2026-06-29] 결정 | 8kw-ev-wpt-tx 다음 시작점 확정 — 블록평균→이동평균 전환

근거: 사용자 결정 (2026-06-29).

- **다음 시작점**: PPB HW 블록평균(N=64) → SW 이동평균 전환 (A5+A6 통합 방향).
  1. `ETA_ADC_OVERSAMPLE_LOG2` 낮춰 실질 85 kHz + SW ring buffer 이동평균 구현.
  2. GUI에서 85 kHz 이동평균 데이터 측정 방법 모색 — 현재 10 Hz 텔레메트리 한계, 방법 미결.
- status.md 다음 시작점 갱신.

## [2026-06-29] 갱신 | 8kw-ev-wpt-tx ADC 샘플링 재작업 (#7·#8) 로드맵 승격

근거: GitHub 이슈 #7·#8 정식 작업 채택 결정 (2026-06-29).

- **roadmaps/adc.md**: §1 마일스톤 표에 A5·A6 추가. §A5·§A6 신설. §6 이슈 백로그에서 승격, #9만 백로그 잔류. date 2026-06-29.
  - **A5 (#7 ADC 실질 샘플링 85 kHz)**: `ETA_ADC_OVERSAMPLE_LOG2`(`src/bsp/eta_bsp_adc.h:28`) 낮춰 85 kHz 실샘플링 달성 + 노이즈 실측. A3.5(N=64 HW-first 확정)와의 방향 재검토 성격 명시. A4와 [추정] 독립(확인 필요).
  - **A6 (#8 SW 이동평균 전환 검토)**: ring buffer 이동평균 — 매 샘플 갱신·스파이크+노이즈 동시. A5 선행 필요. CPU 부하 실측(R5F @400 MHz, 85 kHz×6ch ≈ 510k ISR/s ≈ 784 사이클/ISR [추정]).
  - A5·A6은 "HW N↓" ↔ "SW 이동평균 보완"이라는 한 트레이드오프의 양면.
- **status.md**: 다음 시작점에 A5(#7) 후보 추가. 구현 현황 표 A5·A6 행 추가(✗). 미결 사항 #7·#8 승격 항목 추가. date 2026-06-29.

## [2026-06-26] ingest+갱신 | 8kw-ev-wpt-tx 개발환경 통합·정리 (PR #10) 환원

근거: 커밋 50205b9·67eac11·dc33324·9598a6d·b4e3591 직접 분석 (2026-06-26). [[devenv_roles]] 신설 + 기존 3페이지 갱신.

**devenv_roles.md 신설 (8kw concepts)**: 역할 분리 전체 그림 + 비자명 사실 4개 —
① CCS 디버그는 `build/*.out`만으로 성립(실보드 확인, 빌드 단일화 근거)
② ccs-debug MCP는 CCS IDE GUI 상주 필수, flash와 양립 불가(XDS110 경합)
③ CCS 2100 = Eclipse Theia, 정품 MS VSCode 디버그 어댑터 없음 → VSCode 디버그 이전 비권장
④ enet/sdl 생성물 12개 안전 삭제 근거(`example.syscfg` 미사용·gmake `FILES_common` 불포함·`src/` 참조 0건)
OS별 flash 진입점 확정(Linux `run_flash_node_8kw.sh:7` `~/ti/ccs2100`·Windows `run_flash_node_8kw.ps1:5` `C:\ti\ccs2100`), VSCode clangd 셋업(`build/makefile:138` `-MJ` + `:180-190` 조립·`.vscode/settings.json:2` `--query-driver`), GUI shim 제거(67eac11 `python tools/gui/launch.py` 단일 진입점).

**build_methods.md 갱신**: 제목·리드 문단 재작성(gmake 단일 통합 반영), §1 표 "CCS IDE 휴면" 명시, §4 소스 등록 "gmake만 등록" 단순화, §5 flash `-Source` 인자 제거+OS별 명령 추가, §6 "향후 방향 미정" → "완료(PR #10)" 확정, §7 VSCode clangd 신설, "함께 보기" [[devenv_roles]] 추가.

**ospi_flash_tooling.md 갱신**: §1 위치(`run.bat`+`launcher.mjs` → `run_flash_node_8kw.{sh,ps1}` 대체), §3 진입 구조 전면 재작성(`-Source` argv 소멸·항상 `build/` 고정·SBL `TI_DIR` 환경변수 경로), §5 FACT `-Source` → `build/` 고정 갱신.

**gui_launch_architecture.md 갱신**: §1 shim 2개 삭제·다이어그램 단순화(PR #10 67eac11).

## [2026-06-26] ingest | 8kw-ev-wpt-tx GitHub 이슈 #7·#8·#9 wiki 저장

근거: GitHub 이슈 텍스트 직접 인입 (2026-06-26).

- **roadmaps/adc.md §6 신설 (이슈 백로그)**: #7·#8 추가.
  - **#7 ADC 실질 샘플링 85 kHz 확보** — 현재 N=64 블록평균이 실질 샘플링을 1.33 kHz로 깎음. 손잡이=`ETA_ADC_OVERSAMPLE_LOG2` → 0으로 내려 노이즈 실측. 노이즈 과대 시 #8로 이동.
  - **#8 HW 블록평균 → SW 이동평균 전환 검토** — ring buffer 이동평균, 매 샘플마다 갱신. CPU 부하 추정 ~784 사이클/ISR(R5F @400 MHz) [추정]. #7 선행 필요.
- **it6600c_wifi_gui.md 신설 (8kw concepts)**: #9 IT6600C WiFi 연동 GUI. 당장 착수 예정 없음, 이어가기 위한 기록. SCPI over LAN, 권장=Python+pyvisa+Tkinter, 미결=VISA 주소·명령셋.
- **index.md** `[[it6600c_wifi_gui]]` 등록.

## [2026-06-25] ingest | eta-meta plugin (저작 메타 층) 환원 — 5페이지 신설

근거: `~/eta/eta-ai-tools`(branch feature/eta-meta-skill-creator) 직독 — `eta-meta/skills/skill-creator/SKILL.md`·`eta-meta/agents/reviewer.md`·선례 `eta-harness/skills/planner/SKILL.md`·`agents/verifier.md`·`.claude-plugin/marketplace.json`·`eta-meta/.claude-plugin/plugin.json`·`README.md`. 자리 결정: 펌웨어 도메인 wiki에 툴링/메타 자리가 없어, 스키마상 cross-team 방법론 홈인 루트 `pages/concepts/`에 신설 + index.md 새 그룹 "AI 툴링 / 저작 메타".

- **eta_meta_authoring_layer.md 신설**: eta 마켓플레이스 plugin 셋(짠다/변환한다/짓는다) 중 eta-meta = 저작 메타 층. 왜 별도 층인가(메타 작업을 펌웨어 harness에서 떼어냄)·앞으로 command·agent creator 입주.
- **harness_engineering_principles.md 신설**: 책 세 원리 = 단일 설계 기준. 원리1 Push 3단계·원리2 Progressive Disclosure(분리 3신호)·원리3 Why-First(일반화·컨텍스트 절약 3원칙·명령형). 루브릭 단일 소스=skill-creator(런타임)·비대칭 호명.
- **skill_creator.md 신설**: 세 원리 도그푸드·런타임 루브릭. 의도적 삭제 3종(house 골격 강제·그릇 판별 게이트·TEMPLATE.md)과 왜.
- **skill_authoring_pipeline.md 신설**: author→review→verify→deploy. 단계 성격이 그릇 가름(stance/서브에이전트/워크플로). review(준수)≠verify(효능). verify 미구현(2026-06-26 설계)·충실도 한계.
- **skill_reviewer_agent.md 신설**: 네 결정(서브에이전트 그릇·런타임 루브릭·안티패턴=렌즈·비대칭 해소). 초안·미검증.
- **확정/미정 가름**: skill-creator=완성·커밋됨 / 파이프라인=설계 합의됨(verify 미구현) / reviewer=초안·미검증 — 각 페이지 frontmatter `status`로 표기.
- **발견된 drift 2건(코드 기준 호명, eta_meta_authoring_layer에 기록)**: ①README "플러그인 2개"로 eta-meta 누락(marketplace.json은 3개) ②manifest description의 "house 골격" 문구가 SKILL.md 실제 범위(house 골격 삭제됨)보다 뒤처짐. 정본=코드(SKILL.md). repo 수정은 별도 작업, 미실행.

## [2026-06-25] ingest+lint | 8kw-ev-wpt-tx GUI 런치 구조 신설 + pc_monitor_gui 정정 4건

근거: `tools/gui/`(launch.py·run-gui-{linux.sh,windows.bat}·gui.py) main 직접 확인(launcher commit `316e649`·gui.py `bec434d`, 탐색 2026-06-25). 대상: [[gui_launch_architecture]](신설), [[pc_monitor_gui]]·[[build_methods]]·[[windows_bat_ps1_launcher]]·[[index]] 정정.

- **gui_launch_architecture.md 신설(8kw concepts)**: "어떻게 띄우나 + 왜 안 바꾸나". ①런치 구조=OS 무관 `launch.py` 부트스트랩(repo루트 2단계 위 해석·`.venv` 자동생성 `with_pip`·requirements 설치·venv python 실행·cwd=repo루트·argv passthrough, venv python 경로 OS분기) + thin shim 2개(launch.py 단일 소스). ②deadtime=write(`eta_tuning.h` regex, 100~500ns)→build(`gmake -C build all`)→flash(`tools/ospi_flash/run_flash_node_8kw.{ps1,sh}` OS분기) ⟹ **firmware 소스트리+build/+CCS+JTAG 개발등급 환경 의존**. ③결정=현행 유지, 브라우저/PyInstaller exe/단일명령 통합 불채택(제로설치 청중 부재·단일 아티팩트 번들 불가·OS 양쪽 더블클릭 단일파일 메커니즘 부재). ④lint(README). ⑤가설/모름.
- **pc_monitor_gui.md 정정 4건(2026-06-25 main 실측 staleness)**: ①dead-time 범위 **100~400→100~500** ②FLASH_SCRIPT 경로 **`tools/jtag_flash/`→`tools/ospi_flash/`** + `.sh` OS 분기 추가(`powershell -File` / `bash`) ③gmake 탐색 "PATH→C:\ti 2단계"→**config.mk CCS_PATH 1순위 3단계** ④**PyInstaller exe 종전 "8kw-gui.exe ~39 MB 존재" 서술 무효** — `.spec`·`dist/`·exe 전부 repo 부재(frozen 분기·.gitignore만 intent-trace). 백로그 #4(배포 형태)=py+런처로 **결정됨** 처리. 런처 참조 `gui.bat`/`launch_gui.ps1`→`launch.py` 갱신·date·source 갱신.
- **build_methods.md**: 방법2 진입점 `gui.bat→launch_gui.ps1`→`run-gui-{os}→launch.py`로 갱신 + [[gui_launch_architecture]] 링크.
- **windows_bat_ps1_launcher.md**: 8kw 적용례 historical 표시(`gui.bat`/`launch_gui.ps1` repo 제거·`316e649` cross-OS 전환). cmd 토크나이저 함정·.ps1 UTF-8 BOM은 Windows 전사 공통 지식으로 보존. 함께보기에 [[gui_launch_architecture]]·[[linux_migration]] 추가.
- **확인된 사실(file:line 실측)**: 현재 브랜치 **main**(README:3 "이 브랜치(`ubuntu`)" 오기)·README §6 GUI 실행=수동 pip3+`python3 gui.py`만(launch.py 미언급)·flash 스크립트 `tools/ospi_flash/`에 `.ps1`+`.sh`+`.js` 공존. README 수정은 repo 작업(별도, 미실행).

## [2026-06-24] 환원 | 트렁크 기반 Git 워크플로 실습 → walkthrough 신설 + 표준 4건 보강

근거: g-8kw-ev-wpt-tx에서 트렁크 기반 워크플로를 사이클 3바퀴 직접 돌린 실습 세션(2026-06-24) + repo 직접 확인(git log·tag·ci.yml·PR 템플릿·치트시트). 대상: [[firmware_git_workflow_walkthrough]](신설, 루트 `pages/concepts/`), [[firmware_git_workflow]](§3.1·§5·§8.4·§9 보강 + walkthrough 상호링크), [[index]](2행).

- **firmware_git_workflow_walkthrough.md 신설**: 초심자가 한 사이클을 따라 돌리는 실전 가이드. 8단계 골격 표(가지→커밋→push→PR→CI→merge→삭제→태그, 각 무엇을/왜/게이트) + 실습 3사이클(B 연습 squash `5ea8623`→`e76019b` #3 / A 실전 rebase 7커밋 `726008a..bec434d`+annotated `v0.1.0` / C PR 템플릿 squash `8158e24`→`6d0556a` #4). **흔한 오해 박스**: 로컬/원격 경계(가지·커밋=로컬, push가 첫 원격 접촉, trunk 진입은 merge뿐)·왜 pull request(받는 쪽 관점, `git request-pull` 유래, GitLab=MR)·PR≠커밋 메시지(git/커밋 단위 vs GitHub/가지 전체+리뷰·CI)·PR 컨벤션(Conventional Commits는 커밋 규약, PR 공식표준 없음, squash면 PR 제목=커밋 메시지)·PR 템플릿 펌웨어 항목(영향 타깃 MCU/보드·실보드 HIL·위험/안전 PWM·deadtime·전류·열·폴트). 결정·함정·치트시트 포함.
- **표준 4건 보강(실습 합의 → 표준 반영)**: ①§3.1 신설 **머지 방식**(squash 기본/rebase atomic 예외/merge commit 금지 + squash·rebase 후 `rev-list --count` 깨짐 경고) ②§5 보강 **pre-1.0(`v0.x.y`)=불안정/테스트 grade, `v1.0.0`=첫 production, 테스트/production은 버전번호로 구분, `-rc` 접미사** ③§8.4 신설 **CI informational→required 승격**(branch protection Require status checks, 트리거=안정 green+상시 러너 systemd) ④§9 보강 **보드 구우면 무조건 태그**(HW 테스트 빌드 포함, 추적성).
- **함정 점검**: ①squash/rebase 머지는 GitHub이 새 SHA로 재작성 → `git rev-list --count main..<branch>==0` 규칙 깨짐(로컬 ff-merge만 통함), `gh pr view`=MERGED로 확인·삭제는 `git branch -D`. ②stale 가지(adc) 작업트리엔 CONTRIBUTING.md 부재(분기 이전 커밋) → 탐색은 base 브랜치 기준. ③**ci.yml "§8/§8.1" 인용 점검 결과 = 현재 wiki와 일치**(06-23 번호 재배열로 §8=CI 빌드 게이트·§8.1=왜 확정. 실습 노트의 "§8=실무주의·오기" 우려는 06-23 *이전* 번호 기준이라 이미 해소). → 추측으로 "오기" 기록하지 않고 검증 결과 그대로 남김.
- repo 확인 사실: 태그 `v0.1.0`@`bec434d` annotated("HW 테스트 빌드" 명시), `.github/workflows/ci.yml`=self-hosted informational(`gmake -C build clean→all→.mcelf` + 아티팩트 업로드), `.github/PULL_REQUEST_TEMPLATE.md`·`docs/git-workflow-cheatsheet.md` 존재. 최종 상태 열린 PR 0·원격 가지 main만·작업트리 clean.

## [2026-06-23] create | contributing_template — CONTRIBUTING.md 단일 템플릿 (회사 공통)

근거: 사용자 토의(conversation-2026-06-23) — "어느 프로젝트에서도 동일 적용되는 하나의 템플릿". 대상: [[contributing_template]](신설, 루트 `pages/reference/`), [[index]](Reference 1행).

- **단일 템플릿 가능 근거**: git 규칙(PR·Conventional Commits·SemVer·태그·브랜치 위생)은 전사 공통 → 본문 100% 동일. 프로젝트별 차이는 상단 `프로젝트별` 블록(프로젝트명·MCU·툴체인·빌드 명령·CI 여부)뿐. → 복사 후 그 블록만 수정.
- **페이지 구조**: 사용법(복사→블록만 수정→표준 갱신 시 본문 재복사) + 8kw 채움 예시 + 복사용 코드블록(실제 CONTRIBUTING.md). 정본=wiki, repo는 사본. org `.github`/`firmware-ci` 마련 시 승격 경로 명시.
- **CI는 별개**(이번엔 미작성): 단일 *파일* 불가(툴체인·빌드 명령 프로젝트마다 다름) → "재사용 워크플로(`workflow_call`) 골격 + 프로젝트별 caller·툴체인 설치 조각" 구조가 정답. 툴체인 헤드리스 설치는 환원 불가 조각이라 실검증 선행 필요. → 다음 단계.
- GitHub org 개념 설명 차 진행(repo 공동 소유 계정·`.github` repo가 org 전체 워크플로 템플릿 공유). eta org 사용 여부 미확인 → 당분간 wiki 정본.

## [2026-06-23] update | firmware_git_workflow 갱신 — Tier 계층·PR 필수·Conventional Commits·CI

근거: 사용자 토의(conversation-2026-06-23) — "혼자 개발이지만 시스템으로 박아 새 사람이 그대로 따르게". 대상: [[firmware_git_workflow]](갱신), [[index]](1행 갱신).

- **§0 Tier 계층 신설**: 표준은 완성형이라 혼자 단계에 전부 켜면 안 지킴 → "지금 지킬 최소(Tier 1)+트리거 시 켤 스위치(Tier 2·3)". Tier 1=PR 필수·Conventional Commits·annotated 태그+git hash 임베드·최소 CI·repo `CONTRIBUTING.md`. Tier 2=2번째 사람/`v1.0.0`→main 보호+리뷰 require·코드서명. Tier 3=다중 버전→`release/x.y`·Docker/Nix 툴체인 핀+reproducible·west.
- **§3 PR 필수로 변경**(사용자 결정): 혼자여도 feature/*→PR→CI green→self-merge. 사람 오면 리뷰 require 한 스위치로 슬롯인.
- **§4 Conventional Commits 신설**(사용자 결정): `type(scope): 요약`, type별 SemVer 영향표(feat→MINOR/fix→PATCH/build·refactor·docs·test·chore→무영향), `feat!`/`BREAKING CHANGE`→MAJOR.
- **§8 CI 신설**: 개념(깨끗한 서버 빌드=works-on-my-machine 차단·약속→게이트·멀티MCU 폭증 방지), 전제=헤드리스 빌드 가능(프로젝트별 표: 8kw/lp TI `gmake -C build all` ✓ / nRF SES emBuild [추정] / STM32CubeIDE 막힘 [[cubeide_cli_build_trap]]→CI 예외), [[linux_migration]] Ubuntu 러너와 정렬, 최소 시작=빌드까지만(HIL 미룸).
- 번호 재배열(기존 4~9 → 5~11)·내부 cross-ref(§5·§9→§6·§11) 정정. frontmatter date·source 갱신.
- **남은 일(미실행)**: repo 루트 `CONTRIBUTING.md` + 8kw `.github/workflows/build.yml` 작성은 wiki 갱신 후 별도 단계로.

## [2026-06-22] ingest | Windows→Ubuntu Linux 전환 결정·로드맵 (전사 공통 신설)

근거: 사용자 전환 결정(conversation-2026-06-22) + `projects/` 디렉토리 직접 점검(런처·툴체인·레이아웃 사실 확인). 대상: [[linux_migration]](신설, 루트 `pages/concepts/`), `roadmaps/linux_migration.md`(신설, **루트 `roadmaps/` 디렉토리 신설**), [[index]](공통 Living docs 절 신설 + Concepts 1행).

- **linux_migration.md 신설(루트 pages/concepts/)**: 전사 공통 운영 결정 — 모든 펌웨어 프로젝트 개발환경에 걸침. ①결정표(배포판 Ubuntu 24.04 LTS Desktop amd64 GNOME=CCS Theia 공식지원 20.04/22.04/24.04뿐·STM32CubeIDE·SEGGER 커버·2029 지원 / 전략 듀얼부팅→검증 후 윈도우 파티션 회수·**ESP 절대 삭제 금지**(Ubuntu GRUB이 같은 ESP) / WSL2 배제=윈도우 안 쓰려는 동기와 모순) ②동기 3종(윈도우 거부감·장기 Linux 스킬 투자[Yocto/Zephyr/CI/HIL/오픈툴체인]·**Edge AI 장기동인**[즉시 단계 아님]) ③툴체인 4종 portability 평가표(STM32CubeIDE/SEGGER ES 8.28/CCS Theia+TI Clang 5.1.1/Python3+tk — 전부 네이티브 Linux, `.emProject` $(StudioDir) 상대·nRF5 SDK in-repo·CCS 경로 자동재생성, 24.04 함정[libtinfo5는 TICLANG5.1.1 무해·chrome-sandbox 1회성], 프로브 udev 3종) ④런처 포팅 대상(`.ps1`/`.bat`→`.sh`).
- **roadmaps/linux_migration.md 신설(루트 roadmaps/ 신설)**: 단계 spine L1~L8(백업→듀얼부팅 설치→툴4종→udev룰3종→재import·빌드경로 재생성→**검증 게이트 L6**[보드별 빌드·플래시·브레이크포인트 디버깅 통과해야 진입]→런처 포팅→윈도우 파티션 회수). 완료/검증 기준 표·상태기호(전 단계 ✗ 미착수). L6 전까지 윈도우 안전망 유지 원칙. 현재 위치 L0 미착수. 짝 status.md 없어 상태기호로 직접 표기(프로젝트 로드맵의 [[status]] 위임과 다른 점 명시).
- **배치 합의**: 결정/근거 개념은 루트 `pages/concepts/`(스키마 명확), 로드맵은 **루트 `roadmaps/` 신설**(프로젝트 `roadmap.md`가 프로젝트 루트에 사는 것과 평행 — 사용자 합의). index 링크는 다른 로드맵과 동일 path-style.
- **repo 점검 사실(보강)**: 실 레이아웃 `projects/<팀>/<프로젝트>`(c/·g/, task 설명의 flat과 다름). 런처 grep 확인 — 8kw `run_flash_node_8kw.ps1`=`C:\ti\ccs2100\ccs\scripting\run.bat`·`gui.bat`→`launch_gui.ps1`·lp `bp-3351/jtag_flasher/*.ps1` 11개(⚠️ 구 `ccs2050` 경로). config.mk 3줄 wiki와 일치. `projects/c/`에 백업 zip 2개 + 거대 전달본 사본(`oled_tv_software_전달본/`, SES 설치 .exe·nRF5_SDK·oled_tv.zip). build/**/*.bat=Zephyr/west 캐시 무시 확정. pc_uart_gui `uart_gui.py`+PyInstaller `build/`.
- 기존 페이지 백링크 연결(중복 생성 없음): [[windows_bat_ps1_launcher]]·[[ses_build_conventions]]·[[cubeide_cli_build_trap]]·[[st_link_nrf52_flash]]·[[ospi_flash_tooling]]·[[jtag_flash_clean_host]]·[[sdk_ccs_toolchain_migration]]·[[syscfg_build_model]]·[[instruments]]·[[firmware_git_workflow]].

---

## [2026-06-22] 환원 | oled_tv_software 시립대 전달 문서 신설

근거: 기존 페이지 종합(신규 raw 없음). 대상: [[시립대_전달]](신설), [[index]](갱신은 본 lint에서 보강).

- **시립대_전달.md 신설**: 02·03 커스텀 보드(UTO-NBK-52)를 시립대에 전달하기 위한 통합 핸드오버 문서. P1 핀맵(SPI/UART)·P2 구동 확인 절차(전원 순서·LED 정상 판별·comm_st 케이스)·P3 PC GUI 사용법(`rx_gui.exe` 연결·buck 지령·스크린샷).
- 출처 종합: [[spi_pin_mapping]]·[[uto_nbk_52]]·[[st_link_nrf52_flash]]·[[pc_uart_gui]]·[[comm_state_monitoring]].
- ⚠ lint 호명: nRF측 SPI를 NBL 회로도([[schematic_ble_module_board_v01e00]]) CN2 핀번호로 표기 — 사용자 확인상 회로도 기준 확실 정보. [[uto_nbk_52]]의 "NBL 핀맵→NBK 적용 주의" 경고와의 긴장은 회로도 신뢰로 정리.

---

## [2026-06-19] 갱신 | oled_tv_software STEP3 완료 (커스텀 보드 comm_st 재검증) + 팀보고

근거: 실보드 검증(commit `079bdc7`). 대상: [[status]](STEP3 완료·다음 시작점=시립대 전달 준비), [[team_briefing_oled]](6/19 스냅샷), [[uto_nbk_52]]·[[tx_ble_module]].

- **STEP3 완료**: SPI 배선(P0.22/25/26/27) 후 comm_st 4케이스 재검증 + "02만 ON → SPI UP/ESB DOWN" 신규 케이스 확인. 02 `eta_protocol.c` seed 수정 commit&push(미커밋 해소). 03_TX_ble 실보드 검증 완료(ESB PTX 동작·P0.17/18 오실로).
- 다음 시작점 = 시립대 보드 전달 준비(핀맵·구동 절차·GUI 사용법) → 2026-06-22 [[시립대_전달]]로 산출.

---

## [2026-06-19] 환원 | 8kw-ev-wpt-tx 두 가지 빌드 방법 — build_methods concept 신설

근거: 사용자 제공 + 리포 직접 확인 사실 (build/makefile · build/config.mk · tools/gui/gui.py · tools/ospi_flash/run_flash_node_8kw.ps1 · flash_node_8kw.js). 대상: [[build_methods]](신설), [[index]](갱신).

- **build_methods.md 신설**: "이거 어떻게 빌드·플래시하나"를 빠르게 답하는 진입 페이지. 기존 [[syscfg_build_model]](생성물 의존 메커니즘)·[[ospi_flash_tooling]](flash 메커니즘)과 다른 고도 — 개발자 vs HW 엔지니어 워크플로 관점.
  - §1 방법1(CCS IDE managed build→`Release/`, 개발자 편집·디버그) vs 방법2(GUI gmake→`build/`, HW 엔지니어 원클릭) 비교표: 용도/방식/진입점/빌드명령/산출물/플래시 소스. 방법2 진입 `gui.bat`→`launch_gui.ps1`→`gui.py`→`gmake -C build all`, gmake 탐색=config.mk CCS_PATH. CLI 동등 명령(`gmake -C build all` / `python tools/gui/gui.py --deadtime <ns> --write --build --flash`).
  - §2 공통 스택(CCS21/SDK_06/TICLANG5.1.1/SysConfig1.28, 타겟 AM263P4 r5fss0-0 NoRTOS), 머신별 이식=config.mk 3줄.
  - §3 syscfg 생성물 규칙(generated/ 커밋·SYSTEM_FLAG=true 기본 재생성 스킵·example.syscfg 변경 시만 SYSTEM_FLAG=false·gitignore 금지) → 심층 [[syscfg_build_model]] 위임.
  - §4 새 .c 파일 두 빌드 각각 등록(.cproject sourceEntries / build/makefile FILES_common) 강조.
  - §5 플래시 공통 다운스트림(`run_flash_node_8kw.ps1 -Source release|build`, ERASE_ALL→SBL@0x00→app@0x00081000, IDE 미상주 전제, SW1=`0,0,1,1` xSPI 8D SFDP) → [[ospi_flash_tooling]]·[[jtag_flash_clean_host]]·[[ospi_boot_mode_strap]] 위임.
- 추측·미확인 추가 없음 — 리포 확인 사실만.

---

## [2026-06-19] ingest | 펌웨어 Git 워크플로 표준 (전사 공통 concept 신설)

근거: 사용자 제공 표준 문서 (conversation-2026-06-19). 대상: [[firmware_git_workflow]](신설, 루트 `pages/concepts/`), [[index]](갱신).

- **firmware_git_workflow.md 신설**: eta 펌웨어 팀 전사 공통 git 컨벤션 — 단일 프로젝트 결정 아님. 트렁크 기반 개발(`main` 단일 줄기)+annotated 릴리스 태그 모델. 9개 절: ①TBD+태그 채택 ②왜 펌웨어에 태그 필수(재현성·멀티-MCU 시스템 스냅샷)+**§2.1 태그는 소스만 고정·동일 바이너리는 고정 툴체인/의존성 락파일/reproducible build와 함께일 때만** ③일상 흐름표(작은수정/덩어리/배포/복원) ④SemVer(`v0.x.y` 시작·annotated `-a` 필수·lightweight 금지) ⑤핫픽스 forward-only·다중 유지 시 `release/x.y` 전환 ⑥브랜치 위생(merge 후 삭제·`rev-list --count`·`archive/*` 태그 보존) ⑦릴리스 추적성(git hash 임베드·매니페스트·코드 서명) ⑧실무 주의(깨끗한 push된 tip서 태그) ⑨규모 확장 대안(GitHub Flow/`release/x.y`/Git Flow/west).
- 위치 판단: 모든 펌웨어 repo 공통 방법론 → 프로젝트 디렉토리 아닌 루트 `pages/concepts/`([[schematic_ingest_strategy]]와 동급, `source: conversation-*`).
- cross-ref: §2.1 "툴체인 버전이 바이너리를 바꾼다"는 [[sdk_ccs_toolchain_migration]](8kw 실증)와 연결. §2 멀티-MCU 시스템 스냅샷은 [[app_protocol_module]] 3펌웨어 구조 인접.

---

## [2026-06-19] 환원 | 8kw-ev-wpt-tx 신스택 전환 완전 완료 — 도메인 지식 4건 + 상태 갱신

근거: 툴체인 신스택 전환 완전 완료 세션 (2026-06-19, end-to-end PASS). 대상: [[sdk_ccs_toolchain_migration]](§8 추가), [[windows_bat_ps1_launcher]](신설, 루트), [[ospi_boot_console_diagnostic]](§4 보강), [[ospi_boot_mode_strap]](VCC 주의 추가), [[status]]·[[roadmap]](완전 완료 반영).

- **sdk_ccs_toolchain_migration.md §8 추가**: CCS21 자급자족 — 번들 컴파일러/SysConfig/node로 충분, standalone 불필요. config.mk CCS_PATH 배선 구조. makefile CGT/SYSCFG_NODE `:=` 하드코딩은 config.mk 범위 밖. 구 C:\ti orphan 정리 후보.
- **windows_bat_ps1_launcher.md 신설(루트 pages/concepts/)**: cmd .bat + 한글 + chcp 65001 = 토크나이저 파괴(멀티바이트 토큰 쪼개짐). 해법: ASCII 전용 .bat 래퍼 → .ps1 위임. .ps1 UTF-8 BOM 필수(PS5.1 cp949 오독 방지). Python 런처 레시피(py→python 폴백·의존성 자동설치·진단 콘솔). cwd 독립 설계(`__file__` 기준 내부 자원).
- **ospi_boot_console_diagnostic.md §4 보강**: SDK 버전 간 SBL 해시 상이 = cert serial/timestamp 차이(정상). 머신 간 이주 불필요 — SDK prebuilt 직접 복사.
- **ospi_boot_mode_strap.md 보강**: standalone 부팅 검증 = 물리 VCC 전원사이클 필수(JTAG 리셋 = connect GEL 코어 리셋으로 ROM 미실행).

---

## [2026-06-19] 환원 | 8kw-ev-wpt-tx CCS managed-build Phase 2 마이그레이션 실증 — syscfg_build_model 대폭 보강

근거: CCS21 managed-build Phase 2 마이그레이션 실증 세션 (2026-06-19, commit e1aca4f·f3d16ff). 대상: [[syscfg_build_model]](보강).

- **syscfg_build_model.md 보강**: ①낡은 경로 갱신(TI_DIR/CCS_DIR/SDK_DIR→MCU_PLUS_SDK_PATH/CCS_PATH/SYSCFG_PATH, ccs2050→ccs2100, SDK_01→SDK_06) ②dual-build 중복심볼 메커니즘 §1에 명시 ③함정 5종 신설: ④CDT sourceEntries 1차진실(filteredResources 빌드 무력, 재추가entry 제거 필수, e1aca4f) ⑤컴파일러 발견 CCS인스턴스 종속(신버전은 ccs2100에서만) ⑥All Configurations 미설정 시 Debug 구스택 잔존 ⑦CCS post-build genimage 경로도 수정 필요(ignored-error 조용히 실패, f3d16ff) ⑧Theia 기반 CCS=headless build CLI 없음·Resource Filters UI 없음.

---

## [2026-06-19] 환원 | 8kw-ev-wpt-tx MCU+ SDK/CCS 툴체인 마이그레이션 지식 7건 (구조 재정비 + 신규 1건)

근거: toolchain-ccs21-sdk2606 브랜치 실보드 부팅·기능 검증 완료 세션 (2026-06-19). 대상: [[sdk_ccs_toolchain_migration]](갱신).

- **sdk_ccs_toolchain_migration.md 갱신**: 기존 6건을 "증상→원인→해결·교훈" 구조로 재정비 + 신규 §7 추가. ①SDK 릴리스노트 툴체인 표=하한선·상위 스택 빌드·부팅·기능 정상 실증 ②imports.mak CGT 하드`=`·include 이후 `:=` 재정의 ③`?=` 선점·config.mk 둘 다 수정 ④CCS 번들 SysConfig CLI전용·standalone 불필요·SYSCFG_NODE override 충분 ⑤genimage 리네임·SDK example 본뜨기 ⑥workspace 로드≠마이그레이션·손편집 금지 ⑦**빌드 툴 셀렉터 비결정성 — glob 첫 매치 금지, config.mk CCS_PATH 단일 소스로 makefile+GUI 일치시키기**.

---

## [2026-06-18] 환원 | 8kw-ev-wpt-tx MCU+ SDK/CCS 툴체인 마이그레이션 지식 6건

근거: ccs2050→ccs2100, SDK 26_00_00_01→06 마이그레이션 실증 세션 (2026-06-18). 대상: [[sdk_ccs_toolchain_migration]](신설), [[index]](갱신).

- **sdk_ccs_toolchain_migration.md 신설**: gmake 빌드 신 스택 마이그레이션(.out+.mcelf 경고 0)으로 실증된 함정 6종. ①SDK 릴리스노트·minToolVersion이 실제 요구 툴체인 정본(패치업은 프로파일 불변) ②imports.mak CGT_TI_ARM_CLANG_PATH 하드`=`·override는 include 이후만 유효 ③`export VAR ?=`가 config.mk include 앞이면 config.mk 죽은 줄 됨 ④CCS 번들 SysConfig=CLI전용(nodejs/nw/ 없음)·gmake는 standalone 또는 SYSCFG_NODE override 필요 ⑤genimage 스크립트 리네임(genimage_am26x.py→genimage.py)·SDK example makefile에서 정답 본뜨기 ⑥workspace 로드≠툴체인 마이그레이션(.cproject PRODUCTS·superClass로 확인, Project Properties 직접 변경 필요).

---

## [2026-06-16] ingest | 8kw-ev-wpt-tx GUI 왕복 검증·UART5 RX 1바이트 fix·flash 운영 함정

근거: 실보드 검증 세션 (2026-06-16). 대상: [[uart5_rx_polled_1byte]](신설), [[gpio_impl]], [[jtag_flash_clean_host]], [[uart5_packet_protocol]], [[status]].

- **uart5_rx_polled_1byte.md 신설**: SDK `UART_read()` POLLED+NO_WAIT+FULL에서 `rx.count` 미반영 → stale 0x00 버퍼 주입·SOF 탐색 불가. 수정 = `count=1`·반환값 `==SystemP_SUCCESS` 판정.
- **gpio_impl.md 갱신**: GPIO 루프 패턴(`eta_gpio_request_gd_en` enqueue + `eta_gpio_loop` 소비, `eta_gpio_set_gd_en` static 비공개) 명문화. flash_node_8kw.js mcelf mtime 자동 선택 갱신. "Run > Flash Project" 금지 + 올바른 절차. GUI 왕복 검증 완료(미확인 해소).
- **jtag_flash_clean_host.md 갱신**: "Run > Flash Project" 금지 섹션 추가 — SBL 미포함·전원사이클 부팅 불가.
- **uart5_packet_protocol.md 갱신**: UART5 RX 1바이트 함정 링크([[uart5_rx_polled_1byte]]). TYPE=0x10 왕복 검증 완료 표시.
- **status.md 갱신**: UART5 양방향 △→✓. 다음 시작점 = branch gpio 커밋 → PWM P3 보호 착수. 미결 "GUI 왕복 검증 잔여" 해소.

## [2026-06-16] 환원 | 04_tx_control Nucleo 포팅 작업 항목 기록

근거: tx-dummy 브랜치 탐색 세션 (2026-06-16). 대상: [[roadmaps/04-tx-control-dummy]], [[status]].

- **roadmaps/04-tx-control-dummy.md §7 추가**: NUCLEO-F103RB(F103RBT6) 포팅 작업 항목(N1~N4), 미결 게이트(①CubeMX 재생성 정책 / ②Nucleo HSE 크리스탈 실장 여부), 핀 호환성 탐색 결과(SPI2·UART5 동일 핀, PC13=USER 버튼 공유 무해).
- **status.md**: Nucleo 포팅 미결 항목 추가, D1→D2를 포팅 완료 후 선결로 순서 조정.

## [2026-06-16] 환원 | buck 지령 바이너리화 완료·0x51 전파 검증

근거: 2026-06-16 브랜치 merge 세션. 대상: [[uart_command_set]], [[buck_vout_ref_command_path]], [[status]].

- **uart_command_set.md**: `buck <v>` 텍스트 커맨드 제거 기록. `HAL_UART_RxCpltCallback` 0x51 바이너리 분기 소절 추가. 헤더 노트·요약표 갱신.
- **buck_vout_ref_command_path.md**: 입력 경로 다이어그램을 GUI 바이너리 0x51 → `pkt_apply_rx_cmd()` 기준으로 재작성. `pkt_apply_rx_cmd()` 신설 문서화. 코드 연혁 2026-06-16 항목 추가. `cubeide_newlib_nano_float` 의존성 소멸 기록.
- **status.md**: `0x51 Zin·Tx Buck Vout Ref 와이어 전송` △→✓(u16 BE 확정·GUI→03 실보드 검증). D3 e2e 항목 완료 처리. `Uint16 vs i16 잔여 차이` 미결 해소.

## [2026-06-16] 환원 | DK 검증 완료·SPI 배선 핀맵 신설·SpiCommSt DOWN 진단 경로

근거: DK 보드(STM32 Mini Pro + PCA10040) 검증 세션 (2026-06-16). 대상: [[status]], [[spi_pin_mapping]](신설), [[comm_state_monitoring]].

- **status.md** "01 정본 코드베이스 전환 (HSI 64MHz)" △→✓. DK 검증일 2026-06-16, 정본 경로 `OLED_TV_Rx_Module/` (브랜치 merge) 기록.
- **spi_pin_mapping.md 신설**: STM32↔nRF52 SPI 물리 배선 핀 대응표 (SCK PB13↔P0.27 / MOSI PB15↔P0.25 / MISO PB14↔P0.26 / CS PB12↔P0.22). MISO 미연결 증상(spi_rx_pkt 전부 0xFF → 체크섬 불일치 패킷 드롭 → SpiCommSt DOWN) 기술.
- **comm_state_monitoring.md** "SpiCommSt DOWN 진단 경로" 소절 추가: MISO 배선 → spi_rx_pkt 0xFF 확인 → 나머지 배선 → 구조적 결합 순 진단 흐름.

## [2026-06-15] 환원 | UART5 보드단독 검증 세팅 + Korlan/RS485 사용 가능성 정리

근거: 회로도 p.4·p.5 분석 (2026-06-15 대화). 대상: [[gpio_verification_pinmap]].

- **UART5 보드단독 검증 세팅** gpio_verification_pinmap 추가:
  - 필수 전원 2개: **3.3V → CN1.1** (MCU) + **5V → CON2.1** (COMM_P5V, ISOL2 통신측·MAX232). DGND(CN1.27) ↔ COMM_GND는 B3(SHH-1M2012-221) One Point 결합 → 공통 GND 사용 가능.
  - **옵션 A (CON2 RS232)**: USB-to-RS232 → CON2.2(RX)/CON2.3(TX). MAX232 정식 경로. USB-to-TTL 직접 불가(레벨 불일치).
  - **옵션 B (TP17/TP15 TTL)**: 5V-tolerant USB-to-TTL → TP17(SCIB_TX)/TP15(SCIB_RX). MAX232 우회, 5V 신호. COMM_P5V 공급 시에만 신호 유효.
- **Korlan USB2CAN**: CANH/CANL → CON2.4/5 (CANA_H_CN/CANA_L_CN). CAN 비트레이트 탐색(125/250/500/1000 kbps 순차 시도)으로 APB1=32MHz 기준 비트레이트 미결사항 해소 가능. 선결: 정본 펌웨어 CAN 초기화 여부 확인 + R33 DNP → 온보드 종단 없음(Korlan 내장 termination ON 필요).
- **USB-to-RS485**: 이 보드에 RS485 인터페이스 없음 — UART는 RS232(MAX232), 차동 버스는 CAN. 적용 불가.
- SPI 속도 오기 정정: gpio_verification_pinmap PB13 항목 9.0 Mbps → **8.0 Mbps** (PCLK1=32 MHz, HSI 기준).

## [2026-06-15] 환원 | COMM_P5V=5V 정정·CN2 추가·TP15/TP17 절 추가

근거: 회로도 p.4·p.5 vision 판독 + 사용자 정정(COMM_PSV는 오독, 정확한 표기는 COMM_P5V). 대상: [[schematic_rx_regulator_control_board]].

- **COMM_PSV → COMM_P5V 정정**: vision 오독 확인. wiki 내부(ble_module·rx_ble_module)는 이미 COMM_P5V 표기 사용 중 — 이번 live 대화에서만 오독 발생.
- **CN2(@Rx Power Board, COMM_P5V 측) 절 추가**: 종전 CN1만 기록, CN2 누락. p.5 우측 상단 HEADER_2.0mm/28P(TMM-114-06-T-D-SM). 핀27·28=COMM_P5V, 디커플링 C44/C45, 파워 인디케이터 LED5+R54. **이 보드에 COMM_P5V 생성 회로 없음** — CN2 경유 Power Board에서 전원 수신.
- **COMM_P5V = 5V 확정**: P5V이므로 TP15/TP17 신호는 5V 레벨 — 3.3V UART 직접 검증 불가.
- **TP15/TP17 절 추가** (p.4 UI_Comm): TP15=SCIB_RX(외부→MCU), TP17=SCIB_TX(MCU→외부), 둘 다 COMM_P5V(5V) 레벨·MAX232 이전. 3.3V MCU 직접 검증은 ISOL2 MCU측/PC12·PD2 권장.
- 페이지 구성표 04·05 설명 보강(TP15/TP17, CN2, Test Pins 내용 추가).

## [2026-06-15] 환원 | 01_RX_control HSI 전환·정본 코드베이스 교체·SPI 속도 정정

근거: 2026-06-15 실보드 확인. 대상: rx_control·schematic_rx_regulator_control_board·spi_link_reliability·status·index + 신규 sysclk_hsi_transition.

- **HSE 발진 실패 → HSI 전환 확정**: HSERDY 100ms 타임아웃, 부팅 Error_Handler 무한루프 확인. HSI 경로(HSI/2 × PLL×16 = 64MHz) 채택. 72MHz는 물리적 불가. 확정 클럭 트리 (HCLK 64 / APB1 32 / APB2 32 / 타이머클럭 64 / ADCCLK 8 MHz, Flash latency 2) → 신규 [[sysclk_hsi_transition]] 페이지.
- **SPI2 속도 정정**: rx_control "9.0 Mbps (PCLK1=36 MHz)" → **8.0 Mbps (PCLK1=32 MHz, prescaler=/4)** (정본 기준). 구 dev revert 이후 /8 → 4 Mbps. spi_link_reliability "현재 4.5 MHz" 표기도 갱신.
- **CAN 비트레이트 미결 추가**: APB1 36→32 MHz 변경 파급 — 설계 목표 비트레이트 32MHz 기준 재계산·실측 필요. rx_control·status 미결 추가.
- **01 정본 코드베이스 교체**: 팀원(Sean) 전력제어 중심 정본(AppSequence/AppCtrl/Soft MHz, main.c 통합형) 채택. ESB/SPI relay·UART 모니터 발췌 이식. 빌드 통과·실보드 flash 완료(2026-06-15). UART/ESB 실측 미완(△). status 행 추가·다음시작점 갱신.
- **SPI master/slave**: rx_control SPI section은 이미 Master 기술 — 추가 정정 불요. index rx_ble_module 설명에 "STM32 Master 확정" 명기.
- schematic_rx_regulator_control_board RCC 함의 절: HSE 발진 실패 실보드 확인 경고 추가.

## [2026-06-15] 환원+lint | 03 flash 실측 추가 + 보드 정정(02·03=커스텀보드, DK 아님) + DEVICEID 게이트

앞 프로브 정정(386b9fd) 후속 — 새 사실만 반영. 근거: JLink V9.3 Plus(69730359) CLI 실측.

- **03_TX_ble flash 실측 통과**(종전 "추후"): TX_BLE.hex 151,225 B(6fc8b92, SHA256 D5A0A29B…651936), VTref 3.261 V, FICR `0xE9775EC9`, Bank0@0 57344 B, exit 0. (02=RX_BLE.hex 151,209 B, FICR `0x5FE168DA`.) → 분담표 02·03 모두 "실측 통과".
- **★보드 오기록 정정(A)**: 종전 "02_RX_ble = nRF52 DK(PCA10040) 온보드 J-Link / 외부 프로브 불요"는 틀림. 02·03은 **DK가 아니라 같은 커스텀보드 설계 [[schematic_ble_module_board_v01e00]](UTO-NBL-52)의 별개 물리 개체**, 외부 J-Link(69730359)를 CON1(SWD)에 물려 flash. instruments·flash·index·rx_ble_module 정정. (firmware의 BOARD_PCA10040↔BOARD_CUSTOM 빌드토글은 별개 축이라 미수정.)
- **DEVICEID 보드 식별 게이트**: 02·03 외형 동일 → flash 전 FICR DEVICEID[0](`0x10000060`) 확인으로 칩 1:1 가름(02=0x5FE168DA/03=0xE9775EC9). flash 트러블슈팅·board 페이지·gpio_verification_pinmap에 기록.
- lint: gpio_verification_pinmap "별개 PCA10040 보드 2대"(line 48 "커스텀보드"와 자기모순) → "커스텀보드 2대"로 정정. DEVICEID 사실은 board 페이지(MCU 모듈 절)에 정본.

## [2026-06-15] 환원+lint | 프로브 인벤토리 정정(신규 J-Link V9.3 Plus·1050329071 강등) + 식별 규율

근거: 실보드 CLI 실측 (JLink.exe ShowEmuList V9.48, pyocd list, Get-PnpDevice). 대상 [[instruments]]·[[st_link_nrf52_flash]]·index.

- **신규 프로브**: J-Link V9.3 Plus (ProductName "J-Link CE", S/N **69730359**, HW V9.70, FW Dec 13 2022, RDI/FlashBP/FlashDL/JFlash/GDB, VID_1366 PID_0105). **02_RX_ble flash 실측 통과**(Bank0@0 57344 B, FICR 0x5FE168DA, exit 0, dev HEAD 6fc8b92 빌드 SHA256 일치). 03_TX_ble 절차 동치(실측 추후). → nRF52832 정본 프로브로 등재.
- **★정정(모순 강등)**: 종전 인벤토리의 (a) "J-OB v2 = J-Link OB-nRF5340-NordicSemi / S/N 1050329071", (b) "SAM-ICE 24012600은 별개 제3프로브", (c) "둘 공존→SN 충돌→SelectEmuBySN 1050329071 필수"가 2026-06-15 실측과 정면 모순:
  - 1050329071은 ShowEmuList·Get-PnpDevice 미enumerate → **현존 미확인**으로 강등.
  - "J-OB v2" 동글 단독 연결 시 **SAM-ICE/24012600**으로 보고 → 별개 2프로브 전제 재현 불가(같은 유닛 이중기록 추정).
  - "2프로브 공존→SN 충돌" 함정은 전제 미성립 → 강등(단 ≥2 present 시 SelectEmuBySN은 여전히 권장, SN은 실측값 사용).
- **lint 규율 추가**: 프로브 정체·S/N은 메모가 아니라 **매 세션 ShowEmuList(J-Link)/pyocd list(ST-Link) 실측**으로 확정. 사람 별명("J-OB v2") ↔ 펌웨어 정체(ProductName/S/N) 분리 표기. instruments 머리에 명시.
- **트러블슈팅 룰**(JLink): VTref 읽히나 attach 실패 = SWDIO/SWDCLK 스왑·미접촉(속도 무관) / 0바이트 30초 hang = 무전원·미배선(VTref 자체 부재). 두 증상 원인 다름.
- 분담 갱신: 01=ST-Link V2 네이티브 / 02·03 nRF=J-Link V9.3 Plus(69730359). ST-Link+pyocd 폴백은 강등 유지(UID 40004100040000433539594E, 02 FICR read 정상).
- index 2줄(instruments·st_link_nrf52_flash) 설명 동기화. 2026-06-05 history 로그(line 546~)는 append-only라 미수정.

## [2026-06-15] 환원 | CN1 전원 핀 사실 — schematic_rx_regulator_control_board _CN 절

- 계기: 사용자가 OSC 발진 확인용으로 CN1.1=3.3V/CN1.27=GND 주입 중 — 핀배치 검증 요청
- 회로도 p.5(Board_to_Board) vision 판독(450 DPI 크롭): **CN1 = HEADER_2.0mm/28P (TMM-114-06-T-D-SM), @Rx Power Board**. 핀1·2=PD3V3, 핀27·28=DGND 확정 → 사용자 주입점 정확.
- _CN 절에 CN1 커넥터 블록 추가(종전 `*_CN` 신호 목록만, 커넥터 자체·전원/그라운드 핀 미기록). 페이지02 `CON1`(ST-LINK)과 별개 부품 주의 명시.
- 측정 결론: 전원 경로는 맞으나 HSE 발진엔 펌웨어 HSEON 필요(OSC Clock 절 함의 cross-ref).

## [2026-06-15] ingest | OSC Clock (8MHz) HSE 크리스탈 회로 — schematic_rx_regulator_control_board 보완

- 소스: 회로도 PDF p.2 "OSC Clock (8MHz)" 서브블록 (`raw/Rx_OLED_Regulator_Control_Board_260327.pdf`, Sheet 2 of 2, Rev 0.1E00, 2026-03-27)
- 대상 페이지: [[schematic_rx_regulator_control_board]] (기존 source 페이지 환원 — raw 신규 아님)
- 채운 빈자리: 종전 OSC를 신호명 2개(OSC_IN_uC/OSC_OUT_uC)로만 기록 → 회로 방식·부품 추가
  - **방식**: 수동 크리스탈 Pierce 발진(능동 오실레이터 아님). X1 8MHz/5032, C2=C3=22pF(220J/1608), R10 1MΩ(피드백/병렬), R11 0Ω(OSC_OUT 직렬). OSC_IN=핀5/OSC_OUT=핀6. "MCU 가장 근접 배치" 주석.
  - **함의**: 수동 크리스탈 ⟹ RCC_HSE_ON(구동)이 정답, RCC_HSE_BYPASS 아님. HSE 8MHz×PLL=SYSCLK(64MHz, [[pwm_system]] 정합).
- 갱신: 페이지 구성표 p.02에 OSC Clock 서브블록명 보완(종전 "MCU_Peripheral_Section"만), 주요 컴포넌트 표(X1/C2/C3/R10/R11), 신호 인벤토리 OSC_IN/OUT 행(핀5/6·근거). index.md 설명.
- 근거 수준 명시: 전 항목 **회로도 p.2 vision 판독**(400 DPI 렌더 크롭 확인). 부품 정수=실크 마킹, **OrCAD XML 미교차검증**. 결선도 PDF 이미지라 vision 수준. RCC 함의는 회로방식 연역(펌웨어 코드 미확인).
- 판독 노트: 저해상도 1차 판독에서 C2/C3 패키지를 "3216"으로 오독 → 400 DPI 크롭 재확인 시 "1608" 확정(요청 사실과 일치).

## [2026-06-14] lint | c팀 oled_tv_software — 역순 alias broken link·index 누락·TX SPI staleness 정정

c팀 `oled_tv_software` lint. 기계 점검(index↔파일·broken-link·backlink orphan) + 내용 점검(status/code 대비 staleness). orphan 0, status(2026-06-12)는 코드 대비 최신. 실 결함 3건 정정:

- **broken link (역순 alias, 2곳)**: `[[플래싱 가이드|st_link_nrf52_flash]]` — Obsidian `[[타겟|표시]]` 순서가 뒤집혀 없는 페이지 `플래싱 가이드`를 가리킴 → `[[st_link_nrf52_flash|플래싱 가이드]]`로 교정. [[rx_ble_module]]·[[schematic_ble_module_board_v01e00]].
- **index 누락**: [[esb_timing_measurements]](backlink 5)가 index.md에 미등록 → Concepts ESB 절에 등록.
- **TX SPI staleness (모순, 5곳)**: `e706b53`(2026-06-11)이 03_TX_ble `SPI_Loop`를 SPIS로 전면 재작성(△ 실보드 미검증)했고 status.md·[[tx_ble_module]] 표 행엔 반영됐으나, 같은 entity 서술문 4곳 + index tx_ble_module 설명이 옛 "미구현"에 정지 → 동일 페이지 내 모순. 단일 진실(status.md:74)에 정렬. line 30 "비활성 보존"은 1d7f71a 시점 서술이라 시점 정확성 보존 + e706b53 cross-note 추가.
- `roadmaps/<task>` path-style 링크 3건은 false positive(파일 실재) 확인.

## [2026-06-14] distill | lp-am263p — flash_open_facts S6까지 증류 (63c167d 후속 후보 해소)

6/14 g팀 lint(`63c167d`)이 후속 후보로 남긴 "flash_open_facts S6 내용 증류"를 처리. 3-레이어 규약 ②(확정/폐기를 facts에 반영)가 frontmatter·제목·게이트 섹션에서 S3에 멈춰 있던 것을 S6까지 정렬. (확정 사실 표 자체는 라운드별 inline 갱신으로 이미 R38까지 반영돼 있었음 — 메타·프레이밍만 stale.)

- **frontmatter**: tag `s3-blocker`→`s6-blocker`, source에 `(R7~R38)` 추가, date 2026-06-14.
- **제목**: "Flash_open S3 블로커"→"S3→S6 블로커" + 원장 스코프(S3~S6, 현재 블로커 S6) 블록쿼트 명시. S3 history 보존.
- **게이트 섹션** 재프레이밍: "현재 블로커 (R29)"→"게이트 진행 (S3 해소→S6 블로커)". 옛 "R36 현황"(R37 조사 예정) 줄을 S6 현재 서사로 교체 — R36 마스터 정상→R37 H1 확정→R38 "NP 코어 미실행"·전원/리셋/level-shifter/master SPI 배제→현재 최유력 40MHz XTAL(Y1) 미발진(추론)→R39 오실로스코프 실측.
- log/status 교차검증: 확정 사실·폐기 가설은 [[flash_open_diagnostic_log]](R32/R36/R37/R38)·[[status]](R39 Y1 측정 예정)와 정합 확인. CS 프레이밍 정합은 status 미결로 open 유지(폐기 아님).
- index.md flash_open_facts 설명 갱신("S3→S6 블로커 사실 원장").

## [2026-06-14] lint | g팀 전반 — lp-am263p 단계 staleness 정정 (S3→S6 reconcile)

g팀 3개 프로젝트(8kw-ev-wpt-tx·bp-cc3351·lp-am263p) lint.

- **기계적 점검 무결**: index↔파일 1:1(orphan 0). "broken link"으로 잡힌 것은 전부 의도된 것 — source의 "파생 페이지 후보(lazy ingest)" 미생성 마커, living-doc/스키마 참조 컨벤션(`[[adc]]`·`[[CLAUDE]]` 등), 실재 동일-페이지 앵커.
- **8kw·bp-cc3351**: 모순·staleness 없음.
- **lp-am263p 결함 정정**: 프로젝트가 S3→S6로 전진(R28b에서 S3 통과, 현재 R38 "NP 코어 미실행"·1순위 XTAL)했는데 CLAUDE.md·index·porting.md·roadmap.md가 옛 단계(S3 블로커) 또는 모순 스냅샷(S7 도달 중)에 정지. 단일 진실 [[status]](R39 Y1 발진 실측 예정)에 5개 문서를 정렬. 해소된 S3 history(facts/log 제목·porting §1 배경)는 보존. flash_open_facts의 S6 내용 증류는 범위 밖(후속 후보).
- 커밋 `63c167d`.

## [2026-06-12] 환원+lint | 8kw-ev-wpt-tx — standalone OSPI 무부팅 해소: 진짜 원인 = 부트모드 핀 스트랩 미스매치

수개월간 "flash 프로그래밍/cell 영속성/QE bit"로 의심하던 standalone 무부팅의 진짜 원인이 **부트모드 핀 스트랩 미스매치**로 확정·해소(실측). 무효가 된 종전 진술 일괄 정정.

- **FACT (해소, 실측)**: 보드 flash IS25LX256 = **octal-only**(Extended SPI + Octal DDR만; quad/`0x6B`/QE bit 물리적 부재 — `raw/IS25LX256/` 전 챕터 grep 0건). SW1=`1,1,1,1`(OSPI 4S Quad)은 ROM이 `0x6B`(TRM ch05:749) + QE NV SET(ch05:757) 기대 → octal 칩이 디코드 못 함 → ROM read 실패 → UART fallback `'C'` ping (= 그동안의 무부팅 증상). **SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정 → VCC 전원사이클 후 완전 부팅**(SBL→`"Image loading done, switching to application"`→app→`eta_pwm_init` 85kHz→`eta-tx: 8kw-ev-wpt start`).
- **스위치 극성**: UG §2.1.3 Note(`ug:453`) — 스위치 ON = SOP 핀 GND pull = 논리 0. UG Table 2-5(`:463-471`) = TRM Table 5-2(SOP값, `ch05:498-508`)의 비트반전. xSPI 8D SFDP = UG `0,0,1,1`.
- **신규**: [[ospi_boot_mode_strap]] (8kw concepts) — 해소 정본. TRM Table 5-1(`ch05:138`·Note2 `:139` "4S boot is supported on Flash memories that support 0x6B")·Table 5-2·UG Table 2-5·[[is25lx256_datasheet]]·[[is25lx256_vs_spansion_quirks]] §4 cross-link.
- **lint 정정 (무효 진술)**:
  - [[ospi_boot_console_diagnostic]] §3 (a)cell 영속성/(b)QE bit NV 프레이밍 **무효** → strap 미스매치로 정정. §2 triage(C ping=ROM→SBL 실패)는 정확했고 원인 귀속만 틀렸음. §5 route② standalone 부팅 **실증됨**(미실증→해소). gui.py/flash_8kw.js SW1 라벨 `0011` 수정 반영.
  - [[toggle_free_flash_loop]] §②/§③: 부팅 실패는 잘못된 스트랩 때문(flash 프로그래밍 아님). §③ "4S QE 충족" 전제·"06-05 1,1,1,1 부팅" 기록 무효/모순 표시. 굽기 ✓ + 부팅 ✓로 루프 닫힘.
  - [[jtag_flash_harness]] §4 "standalone 부팅 4S `1,1,1,1` 실증" → octal-only 칩에 불가, 정답 스트랩 `0,0,1,1`로 정정. §8·빈자리 갱신.
  - [[flash_open_facts]]·[[sbl_app_flash_handoff]]: **층위 구분** cross-ref만(cc3351 런타임 app `Flash_open()` ≠ standalone 부트 스트랩).
- **모순(미해소)**: 2026-06-05 "SW1=`1,1,1,1`에서 부팅" 기록은 octal-only 칩에 물리적으로 불가 → 라벨 오기 추정([추정]), 당시 물리 스위치 위치 미확정(모름)으로 표시.
- **갱신**: index(ospi_boot_console_diagnostic·toggle_free_flash_loop 설명 갱신 + ospi_boot_mode_strap 신규 등록), log. (status/roadmap: standalone 부팅은 8kw status 현황표 항목 외 — 게이트 미해당, 갱신 없음.)

## [2026-06-12] 환원 | 8kw-ev-wpt-tx — OSPI 부팅 진단 사이클 환원 (부팅 ✗ ROM→SBL 실패 확정 + SBL provenance + flash 블로커)

2026-06-12 진단 세션의 검증된 사실을 wiki에 환원.

- **FACT (부팅 실패 확정)**: COM4(= SoC UART0 콘솔 "XDS110 Class Application/User UART") 115200/8N1 캡처 — `'C'`(0x43) XMODEM ping + ID 블롭(`"AM263PX"/cdab=0xABCD`) 반복·SBL banner·app banner 전무. **판정: ROM→SBL 로드 단계 실패** (TRM ch05:877·:133 — `'C'` ping = ROM만 송신, ROM이 SBL 점프 성공 후에는 ROM 레벨 fallback 없음). 전원사이클 = USB-unplug VCC 완전 제거·SW2/SW3 버튼 안 씀 확인 → §③ 4-byte stuck 경로 완전 배제.
- **FACT (SBL provenance 확정)**: `C:/ti/sbl_ospi_am263p.tiimage`(307005B) = SDK `sbl_ospi_multicore_elf.release.tiimage`와 바이트 동일. 변종(multicore_elf)·실리콘(am263px-lp)·무결성 전부 정합. "SBL 파일 잘못됐다" 가설 완전 제거.
- **잔여 블로커**: flash cell 영속성(readback은 동일 세션 XIP 뷰라 POR 생존 증거 아님) + flash NV config·QE bit 상태 미확인.
- **정정 후보(미수정)**: [[jtag_flash_harness]] §4 banner `eta-tx: 8kw-ev-wpt v1.0e00`는 구 이미지 기준 — 현 `src/main.c`:45는 `"eta-tx: 8kw-ev-wpt start"`. `tools/gui/gui.py`:553 SW1 라벨이 OSPI(4S)=`1,1,1,1`과 DevBoot=`0,1,0,0`을 한 줄에 혼용.
- **신규**: [[ospi_boot_console_diagnostic]] (8kw-ev-wpt-tx concepts).
- **갱신**: [[toggle_free_flash_loop]](source·title·header·§②실패확정·§③VCC확정주석·미확정·함께보기), [[jtag_flash_harness]](§4 banner주석·§8 SBL provenance·빈자리), index, log.

## [2026-06-12] 환원 | lp-am263p — SW3 RESETz(WARMRESETn) 상세 보강 (회로도·UG)

"SW3(RESETn)이 뭐냐" 질의 → UG Fig 2-11·Table 2-4 + 회로도 push-button sheet 조사. [[CLAUDE]] "리셋/푸시버튼" 절을 SW3 중심으로 보강.

- **FACT**: SW3 = **RESETz 푸시버튼 = SoC warm reset(WARMRESETn) 입력**(UG:432, net `AM263P_RESETN_PB`). assert 소스: SW3 비눌림 OR `TA_RESETz`(테스트자동화 헤더 PMOS). 묶이는 곳: SoC WARMRESETN 출력 + **양 Ethernet PHY reset** + μSD load switch(SoC `GPIO122` 2-입력 AND)(UG Fig 2-11:642–656). PORz와 달리 U4 SOP 드라이버 OE엔 안 묶임(SOP 재래치는 PORz 몫).
- **boot 의미**: ROM 관점 cold==warm(TRM:2098, 부트모드 재샘플·ROM 재실행). 단 warm reset은 SoC만 리셋하고 **flash를 POR 못 함**(전 항 SW2와 동일) → 4-byte stuck시 부팅 안 풀림.
- **회로도 위치 추가**: 버튼 3종 SW2/3/4(`COSW2/3/4`)는 sheet 15 `PROC171_Push_Buttons.SchDoc`, PORz 결합로직(AND/U4)은 sheet 6. SW4=INT1=SoC `GPIO123`(net `AM263P_INT1_PB_GPIO123`, TA_GPIO1로도 assert) 보강.
- **갱신**: [[CLAUDE]] "리셋/푸시버튼" 절(SW3 net·assert 소스·warm-reset boot 의미·SW4 GPIO123·push-button sheet 추가), log. (board-common, status/roadmap 무관.)

## [2026-06-12] 환원 | lp-am263p — SW2 PORz 정체 + 버튼 리셋은 flash를 POR 못 함 (회로도·UG)

"LP-AM263P SW2 PORz가 뭐냐" 질의 → 회로도 sheet 6(`PROC171_AM263P_2_Clock_Reset_Boot_JTAG.SchDoc`)·UG Table 2-4·Fig 2-10/2-11 조사.

- **FACT**: SW2 = **PORz 푸시버튼 = SoC Power-On Reset(콜드급) 입력**(UG:431). PORz는 3-입력 AND(3.3V 벅 PG·1.2V 벅 PG·SW2 비눌림)로 생성, PMOS로 TA_PORZ/BP_PORZ도 assert. SoC PORz 입력 + Boot mode State Driver U4 OE(`PORZ_DELAY` RC ~1ms, SOP 핀 tSOP.hold 유지)에 묶임 → 누르면 SW1 부트모드 재래치 + ROM 콜드 재실행. (SW3=RESETz warm reset[Eth PHY·μSD에도 묶임], SW4=INT1.)
- **루프 직결 FACT**: **SW2 PORz·SW3 RESETz 어느 버튼도 OSPI flash를 POR하지 못한다** — 두 리셋 트리에 flash 3.3V도 flash RESET#(`AM263P_OSPI0_RST`, SoC OSPI_RESET_OUT 구동)도 안 묶임. >128Mb flash 4-byte stuck(TRM §5.4.1:530)은 버튼 리셋으론 안 풀림 → **진짜 VCC 제거만 3-byte 복귀**. [[toggle_free_flash_loop]] ②가름 ⓪을 3-way(a 전원차단/b SW2 PORz/c SW3 RESETz)로 정밀화.
- **갱신**: [[CLAUDE]] 하드웨어 절 "리셋/푸시버튼" 신설(SW2/3/4 표·PORz 트리·flash 미연결 경고), [[toggle_free_flash_loop]](§② 가름 ⓪ 3-way·§③ 버튼 둘·운영규칙), index, log. (board-common 사실, status/roadmap 무관.)

## [2026-06-12] 환원 | lp-am263p — 토글-프리 루프 OPEN을 TRM/UG로 조사 (boot 경로 정당 + warm-reset 근본원인 확정)

[[toggle_free_flash_loop]] OPEN을 AM263P TRM §5.4.1·UG·IS25LX256 데이터시트·회로도로 조사(신규 raw 없음 — 기존 ingest 환원). **②의 무토글 관측을 직접 닫지는 못하나, boot 경로 정당성 확정 + "warm-reset chip-state" 근본 메커니즘 닫음.**

- **FACT (boot 경로 정당)**: ① BOOTMODE 핀은 매 POR/reset release 재샘플링(TRM §5.1.1:111·§5.3:480) → SW1=`1,1,1,1` 고정으로 매 전원사이클이 OSPI(4S) 재진입, DevBoot 토글 불요. ② OSPI(4S)는 non-XIP(§5.4.1.3.1.1:761) → ROM이 매 부팅 flash→RAM 새로 복사 → 재flash 이미지가 다음 전원사이클에 반영. ⟹ 토글-프리 루프는 아키텍처상 성립.
- **FACT (warm-reset 근본원인)**: TRM §5.4.1 Note(:530) — >128Mb flash는 warm reset 시 ROM(3-byte)/flash(4-byte) 주소 불일치로 boot 실패, flash RESET#/full POR만 해소, ROM은 SW reset 안 냄. IS25LX256=256Mb·Octal DDR 4-byte 고정(데이터시트:161). 보드는 flash RESET#(`AM263P_OSPI0_RST` R99)을 SoC OSPI_RESET_OUT에 배선하나 ROM은 bare warm reset서 안 건드림. **⟹ 루프 reset은 진짜 VCC 제거(flash POR)여야 하고 SW3 `RESETz` warm reset이면 안 됨** — [[jtag_flash_harness]] §3 "파워 사이클 필수"의 silicon 근거.
- **진단 영향**: ②의 (A)/(B) 가름에 ⓪번 스텝 추가 — 그 "전원사이클"이 VCC 완전 제거였는지 vs SW3 warm reset였는지부터 확정(warm이면 4-byte stuck → A 확정).
- **갱신**: [[toggle_free_flash_loop]](frontmatter source·§② 가름 ⓪·§③ 신설·미확정·함께보기), log. (status/roadmap 게이트 미통과 — 갱신 없음.)

## [2026-06-12] ingest | lp-am263p / 8kw-ev-wpt-tx — OSPI 부트모드 굽기 "토글-프리" 실측 (굽기 ✓ / 부팅 OPEN)

dead-time 반복 워크플로(빌드→flash→전원사이클)에서 SW1 부트모드 토글을 피하는 루프가 서는가. **굽는 절반은 확정, 부팅 절반은 미확정**으로 정직하게 분리 기록.

- **FACT (굽기)**: JTAG flash는 SW1=OSPI(4S)=`1,1,1,1`(DevBoot 아님)에서도 성공 → **굽기에 DevBoot는 필수 아닌 편의**. 근거: SW1=`1,1,1,1`(app 부팅돼 돌던 상태)+CCS IDE 종료에서 run_flash_node_8kw 3/3 OK·EXIT 0. 메커니즘: 매 OP `loadProgram`마다 `"CPU reset (soft reset) ... on program load"` — flasher가 코어 soft-reset해 돌던 app서 점유 인수(flashFixUpOspiBoot chip 1S 리셋과 별개, 코어 점유 해소가 이번 신규 관측). → [[jtag_flash_harness]] §7 신설.
- **OPEN (부팅)**: 굽기 직후 SW1=`1,1,1,1` 유지 전원사이클 → Logic2 PWM 4ch 정적 logic 0·무토글(캡처길이 아티팩트 배제). 미진단 분기 (A)부팅/펌웨어 실패 vs (B)측정 배선(GND 공통·프로브 접촉) — 측정만으론 "신호 0"과 "미결선" 구분 불가. 다음: UART 텔레메트리(독립 부팅 증거)+GND 확인으로 가름. **신규 [[toggle_free_flash_loop]]** (lp-am263p concepts, board-common).
- **정직 표기**: warm-reset 후 chip-state·OSPI 부팅 후 PWM 미관측 근본원인 = 미확정(추론 금지). 2026-06-05 banner는 다른 이미지·세션 증거라 이번 루프 부팅 증거로 전용 금지. 이번 무토글을 commit `4014901` Saleae PWM PASS와 혼동 금지(별개 세션·셋업).
- **갱신**: [[jtag_flash_harness]](frontmatter date·§4 부트모드 주석·§7 신설·빈자리·함께보기), **신규 [[toggle_free_flash_loop]]**, index(harness 1행 §7 추가 + 신규 1행), log.

## [2026-06-12] 환원 | oled_tv_software — SPI/ESB 링크 DOWN 표시 스크린샷 추가 + 더미 데이터 사실 정정

- **raw 추가**: `raw/pc_uart_gui/eta-c-oled-spi-down.png`(SPI DOWN·ESB UP), `raw/pc_uart_gui/eta-c-oled-esb-down.png`(SPI UP·ESB DOWN). 링크 단절 시 상단 링크 표시 DOWN 전환 동작 증빙.
- **더미 데이터 사실 정정**: 직전 스크린샷 환원에서 Physical 변환 수치를 실 데이터처럼 기술했으나 — **수치는 펌웨어 더미 데이터**, FW 버전(11.22/33.44)도 더미. Physical 변환 로직(스케일 계수 테이블)은 구현 완료. 실 센서값 연결은 향후.
- **갱신**: [[pc_uart_gui_verification_260612]](더미 경고·스크린샷 3·4 절), [[pc_uart_gui]](SPI/ESB DOWN 사실·더미 경고), 외부 `업무보고_2026-06-12.md`(더미 명시·DOWN 스크린샷 절 추가), log.

## [2026-06-12] 환원 | oled_tv_software — PC UART GUI 스크린샷 실보드 검증 (6패널·Physical 변환·TX Buck Set E2E)

스크린샷 2종(`eta-c-oled-monitor.png`, `eta-c-oled-tx-buck-set.png`)에서 확인된 사실 환원:

- **GUI 레이아웃 정정**: "2컬럼" 설명을 **6패널 2×3 그리드**(TX/RX Status·Input·Output)로 명확화.
- **Physical 변환 구현됨** (기존 wiki에 미기재): 전압·전류 raw×0.01, 온도 raw×0.1. 실측 — Buck_Vout 1200→12.00V, Stack_Temp 450→45.00°C.
- **FW 버전 표시 확인**: TX Status 상단 "FW: 11.22", RX Status "FW: 33.44".
- **활성 비트 굵게 표시**: Tx_Sys_Init_St·Tx_Sys_Rdy_St·SPI_Comm_St·BLE_Comm_St·TxVbus_Steady_St·TxBuck_RunStop_St = 1 확인.
- **TX Buck Set E2E 실측 확인**: GUI `222.22V` → `Sent: buck 222.22` → 0x51 Tx_Buck_Vout_Ref=22222(raw)/222.22V(Physical) → 03_TX_ble SEGGER 터미널 `Tx_Buck_Vout_Ref=22222` 직접 확인. 3보드(COM17), SPI UP + ESB UP.
- **신규 raw**: `raw/pc_uart_gui/` (이미지 2종). **신규 [[pc_uart_gui_verification_260612]]** (Sources). **갱신**: [[pc_uart_gui]](레이아웃·Physical·FW·E2E·날짜), [[team_briefing_oled]](스냅샷·2-2절), 외부 `업무보고_2026-06-12.md`(스크린샷 절 추가), index(pc_uart_gui·sources 1행), log.

## [2026-06-12] briefing | C팀 oled_tv_software — 주간 업무보고 2026-06-12 (6/5~6/11)

- **신규 [[team_briefing_oled]]**: C팀 oled_tv_software 업무보고 living-doc 신설 (G팀 선례 동일 패턴).
- **외부 파일**: `C:\Users\echog\eta\업무보고_2026-06-12.md` 생성.
- **보고 핵심(6/5~6/11)**: ① SPI·ESB comm-state 비트 2개 실보드 검증 완료 ② PC UART 바이너리 모니터 + GUI 완성·검증 ③ 코드 정리 3종(app_protocol 적출·02 리팩토링·_shared 다듬기) ④ 04_tx_control 더미 신설(E2E 준비).
- **갱신**: [[team_briefing_oled]](신규), index(Concepts 1행), log.

## [2026-06-11] 환원 | 8kw-ev-wpt-tx — PWM 레그2 dead-time 정밀화 + EPWM0 fan-out + 레그2 동형화

branch pwm-deadtime, commit 4014901. EPWM0 더미 마스터 fan-out + 레그2 isoform AQ + 2-compare 합성으로 dead-time 비대칭 ~22 ns→±2 ns, 레그1·레그2 동형 완전 확인.

- **신규 [[pwm_leg2_isoform_report]]** (`pages/sources/`): 4-DT sweep(100/150/250/400 ns) 검증 리포트 + `raw/pwm_leg2_isoform/` 원본 데이터(digital.csv×4 + analyze.py×3 + capture.sal).
- **핵심 토폴로지 변경**: 구(EPWM4 0-hop / EPWM7 1-hop) → **신(output-less EPWM0 → EPWM2/4/7 전부 1-hop)**. TBPHS trim 불요. gEpwmTbClkSyncDisableMask에 EPWM0 자동 포함.
- **레그2 isoform**: EPWM4_A CMPA=TBPRD/2+DT·CMPB=TBPRD/2 / EPWM7_B CMPA=TBPRD/2−DT·CMPB=TBPRD/2. ETA_DEADTIME_NS 단일소스 자동 추종.
- **검증 결과**: 비대칭 ≤4 ns(5 ns 양자화 바닥), 4에지 시차 ≤2 ns, high-time 4채널 완전 일치, shoot-through 0(전 구간).
- **갱신**: [[pwm]](§3 P2 EPWM0 fan-out 서브섹션 + §비대칭 해결됨), [[am263p_epwm_module_sync_deadtime]](패턴·검증·8kw 인스턴스·스큐 0 토폴로지 검증됨), [[am263p_epwm_sync_topology]](검증 질문 확인·토폴로지 표 갱신), [[pwm_pinmap]](비대칭 ~22 ns→±2 ns), [[status]], index, log.

## [2026-06-11] ingest | lp-am263p — EPWM Time-Base Counter Synchronization (§7.5.6.4.3.3) + fan-out 스큐 토폴로지

TRM EPWM sync 본문 보완 요청. **핵심 발견: 본문 누락 아님** — raw `ch07_5_controlss.md` :5683–5953은 PDF pp.651–654를 충실 재현(끊긴 cross-ref ":5801 Refer to **for** a list…"는 PDF p.652 TI 원본 버그, 추출 손실 아님). PDF figure 7-181/7-182를 직독해 환원.

- **신규 [[am263p_epwm_sync_topology]]**: ① SYNC는 **모듈별 독립 MUX(fan-out)**, 데이지체인 아님 — `EPWMSYNCINSEL`로 공용 SYNCOUT 풀(Table 7-154: EPWM0~23/ECAP0~9/INPUTXBAR/TIMESYNCXBAR/FSI)에서 소스 1개 선택. ② source→target **hop당 지연 고정**(`TBCLK==EPWMCLK`→2×EPWMCLK, `TBCLK<EPWMCLK`→1×TBCLK), **target 인덱스 무관·누적 없음**. ③ Figure 7-181(SYNCIN MUX·SYNCOUT 로직·SYNCPER)·7-182(EXTSYNCOUT 8 PLLSYSCLK stretch) 직독. ④ 레지스터 표(PHSEN/PHSDIR/TBPHS/PRDLD/PRDLDSYNC/SYNCOUTEN/EPWMSYNCINSEL/EPWM_CLKSYNC/one-shot).
- **검증질문 답**: EPWM2 SYNCOUT을 EPWM4·EPWM7이 각각 fan-out 선택 → **둘 다 1-hop·같은 지연 → 상호 정수클록 스큐 0**(잔여 sub-clock은 TRM 모델 밖, 미검증 예측). 8kw ~11ns 비대칭의 정체 = master 0-hop vs slave 1-hop = 2×EPWMCLK(≈10ns @prescale 1, 200MHz) + 라우팅 ~1ns.
- **Table 7-153 "synchronization order" 해소**: 가리키는 실체는 §7.5.6.4.3.3 = Figure 7-181 MUX + Table 7-154 선택행렬. **device-specific sync-order/체인 표는 TRM에 부재**(SPRUJ55D).
- **갱신**: [[am263p_epwm_module_sync_deadtime]](§함정 "모듈간 위상 스큐" 근본=hop 수 비대칭으로 재서술 + fan-out 0-스큐 토폴로지 추가), [[am263p_trm]](Ingested 섹션 등록 + 본문 누락 없음 확인), index, log.

## [2026-06-11] 환원 | 8kw-ev-wpt-tx — UART5 PC 텔레메트리 (18B 바이너리 패킷 + PC GUI)

UART5로 ADC 6채널을 PC에 송출하는 바이너리 패킷 + 호스트 GUI 작업 환원 (branch uart5, commit ba241fa·979699d, 실보드 검증 2026-06-11). c팀 oled 선례([[pc_uart_gui]]) 형식 참조.

- **신규 [[uart5_packet_protocol]]**: 18B 고정 big-endian `[SOF=0xA5][LEN=12][TYPE=0x01][SEQ][ch0..ch5 raw u16][CRC-16/CCITT-FALSE]`, CRC poly 0x1021·init 0xFFFF·범위 byte[1..15]. RTI2 10Hz·115200/8N1 polled blocking. thin device(wire=raw only)·smart host(mV=raw*3300/4095 미러). 채널 순서=ETA_ADC_CH enum, `eta_packet.c` 직렬화 자동 추종. SOF동기+CRC 1바이트 슬라이드 재동기. 선례 대비 CRC-16·단일 패킷·단방향.
- **신규 [[pc_monitor_gui]]**: `tools/gui/gui.py`(pyserial+Tkinter+matplotlib). 4컬럼 표(Channel/ADC(V)/ADC(12bits)/Physical)·채널 체크박스(플롯·CSV 토글)·패킷 헬스(Hz/SEQ드롭/CRC에러)·라이브 플롯·raw-only CSV·PyInstaller 단일 exe. Physical 계수 테이블 단일 소스(계수 미입수 placeholder).
- **검증**: COM13(CP210x, J1.4→THVD1400→J24) 29.8s — 10.067Hz, 301프레임 전부 유효, SEQ 드롭 0·CRC 에러 0. 프레이밍 강건성(정상/1바이트 손상→재동기/ASCII 잡음·가짜 SOF→폐기 후 복구) 모두 PASS.
- **미결 해소**: A1.5 UART 출력 채널 하드코딩(`DebugP_log`) → `eta_packet.c` 채널 루프 직렬화로 대체(자동 추종).
- **신규 잔여**: UART5 송신 논블로킹화(현재 polled blocking), 물리량 변환 계수 미입수(GUI Physical placeholder), RS-485 Phase 2.
- ⚠️ **핸드오프 프롬프트 전제 정정**: "wiki 루트 빈 슬레이트, status.md 신규" → 오류. 실제로는 ADC(A2)·PWM(P1/P2) 이력이 가득한 기존 디렉토리 → status.md는 **갱신**(덮어쓰기 아님), concept 2개만 신규.
- **갱신**: [[status]](UART5 텔레메트리 직전완료 절·구현현황표 행·미결사항), [[roadmap]](§2 별트랙 완료), index, log.

## [2026-06-11] 환원 | oled_tv_software — 04_tx_control 구현 결과 반영 (e706b53·07fbf1f)

로드맵 전제와 실 코드 간 어긋남 5개 정정 + 구현 결과 환원:

- **정정 1**: 03 SPI_Loop = SPIM 코드 → SPIS 전면 재작성(e706b53, 02 거울, nrf_drv_spis MODE_2)
- **정정 2**: ADD_SPI 이미 emProject에 정의됨
- **정정 3**: pkt_apply_rx 없음 → pkt_print_data_line raw 출력으로 마감
- **정정 4**: g_rx_data 없음 → g_last_ack_by_hdr[3]
- **정정 5**: 검증 기준 "12.00V" → raw 1200 (pkt_print_data_line ÷100 안 함)
- 현황: 03 SPIS △(emBuild ✓), 04 △(07fbf1f, CubeIDE 빌드 미수행). D2·D3 미수행.
- **갱신**: [[roadmaps/04-tx-control-dummy]](§4 신설·§2 마일스톤), [[status]], [[tx_ble_module]], log.

## [2026-06-11] 계획 | oled_tv_software — 04_tx_control 더미 작업 호 신설

03_TX_ble SPI_Loop 활성화 + STM32 더미(04_tx_control, 01 기반) 신규 작업 호(D0~D3) 신설. 최종 목표: 01의 TX Buck Vout Ref → 04 UART 모니터 E2E 검증. 구현 세션 핸드오프 프롬프트 [[roadmaps/04-tx-control-dummy]] §4에 수록. index 갱신.

## [2026-06-11] 환원 | oled_tv_software — _shared 프로토콜 다듬기 완료 (9ad338d·99c893f)

커밋 9ad338d(실보드 검증)·99c893f(실보드 검증)의 사실을 6개 파일에 환원:

- **패킷 크기 정정**: `prd.md` "56B/45B, HDR 0xC0" → "wire 11B, 컨테이너 43B/54B; HDR 0xC0은 구 표기"
- **공유 API 표면 재서술** ([[app_protocol_module]] §_shared): 잔존 8함수 표 신설. 제거 심볼(`pkt_print_comm_line`·`pkt_apply_rx`)·01 `calc_checksum` 통일 기록.
- **3펌웨어 표준 패턴 갱신** ([[app_protocol_module]] §3펌웨어): 섹션 헤더 "03 예정" → "02·03 완료", 모듈 표 `app_*` → `eta_*`(02/03 nRF52 접두사).
- **round-robin 상수 신설** ([[spi_packet_format]]): `PKT_KIND_COUNT=3`·`PKT_RR_STATUS/INPUT/OUTPUT=0/1/2`·`PKT_DATA_FW_OFFSET=6` 절 추가.
- **SPI_COMM_ST_MIN_COUNT 제거 기록** ([[comm_state_monitoring]]): `9ad338d`에서 삭제됨(참조 0건). `pkt_print_comm_line` 섹션 헤더 "orphan" → "9ad338d 제거".
- **status 갱신**: 다음 시작점에서 `_shared` 레이어 완료 표시, 프로토콜 테이블 2행 추가(_shared 완료·02 텍스트 모니터 검증), 미결 사항 `_shared` 매크로 점검 행 제거.
- **roadmap 갱신**: §3 `_shared` 완료 ✓, §5 매크로 점검 완료 표시.
- **갱신**: [[status]], [[roadmap]], [[app_protocol_module]], [[spi_packet_format]], [[prd]], [[comm_state_monitoring]], log.

## [2026-06-11] 환원 | oled_tv_software — 03_TX_ble 리팩토링 완료 + nRF52 코딩 관습 추가

- **03_TX_ble 리팩토링**: 1d7f71a, emBuild 에러 0·경고 0. 02와 동일 6개 eta_ 모듈 구조. 실보드 미검증. SPI_Loop 비활성 보존.
- **nrf52_firmware_conventions 추가**: 모듈 의존 방향(protocol→{esb,spi,clock,gpio} 단방향)·Monitor baseline-delta(unsigned wrap 무해)·ESB health 독립 판정(02=rx_cnt, 03=ack_cnt) 절 신설.
- **tx_ble_module**: DBG_PIN_TX_ATTEMPT/DONE 심볼 추가, 03 리팩토링 행 추가.
- **갱신**: [[status]](다음 시작점·02 행 ✓·03 행 △·미결 사항), [[roadmap]](§3 별트랙 03+_shared 다음), [[nrf52_firmware_conventions]], [[tx_ble_module]], log.

## [2026-06-11] 환원 | oled_tv_software — 02_RX_ble 정리 도메인 사실 (채널 분리·GPIO 구분·코딩 관습)

코드만으로 드러나지 않거나 펌웨어 CLAUDE.md와 어긋난 4가지 사실 환원 (b92835c→e85839c):

- **[1] 모니터링 채널 분리**: 01 UART5 = 11B 바이너리(기계 파싱 계약, uart_gui.py), 02 Monitor_Loop = 사람 텍스트(디버그 터미널, 기계 파서 없음). 02 코드 수정은 GUI 무관. [[comm_state_monitoring]] "모니터링 채널 분리" 절 신설. CLAUDE.md 갱신 후보 표시.
- **[2] GPIO P0.17/18 구분**: "P0.17/18 = ESB 토글 핀, 제거 금지"는 **03_TX_ble 한정**. 02_RX_ble DK에서 P0.17/18/19는 LED1/2/3(System Ready·SPI_Comm_St·BLE_Comm_St). [[rx_ble_module]] "GPIO 핀 현행" 절 신설, [[tx_ble_module]] 경고 주석 추가. CLAUDE.md 갱신 후보 표시.
- **[3] nRF52 코딩 관습** 신규 페이지 [[nrf52_firmware_conventions]]: ISR printf 금지(HardFault 실증)·오류 카운터 패턴(1초 윈도우 블록 끝 append)·init 배너 printf 금지·eta_ 접두사([[nrf52_module_naming]] 위임).
- **[4] NRF_LOG/SEGGER_RTT 잔재**: 02_RX_ble init 코드만 존재·호출 0건. 무해하나 신규 정리 시 혼동 주의. [[nrf52_firmware_conventions]] 수록.
- **갱신**: [[comm_state_monitoring]], [[rx_ble_module]], [[tx_ble_module]], index, log.

## [2026-06-11] 환원 | oled_tv_software — nRF52 모듈 네이밍 관습 + SES emProject 가상 폴더 확정

- **[1] nRF52 로컬 모듈 `eta_` 접두사 규칙** (`b92835c`, 빌드·실보드 검증 완료): `app_`은 nRF5 SDK 네임스페이스(`app_uart`/`app_timer`/`app_fifo` 등 다수)라 로컬 모듈과 충돌. `eta_`로 근본 제거 — 헤더/소스 이름 대칭 회복(`eta_uart.h`+`eta_uart.c`). 적용 범위: 02_RX_ble 완료, 03 후보, 01 해당 없음. 신규 페이지 [[nrf52_module_naming]] 작성.
- **[2] SES `.emProject` `<folder>` 가상 그룹 확정**: `<folder Name="...">` 는 Solution Explorer 표시 전용 — `file_name`·`c_user_include_directories`를 건드리지 않는 한 빌드·디스크 경로 무영향. [[ses_build_conventions]] §4 추가.
- **갱신**: [[ses_build_conventions]](§2 해소 처리·`eta_` 전환 경위·§4 가상 폴더 신설·관련 링크), index, log.

## [2026-06-10] 갱신 | lp-am263p·8kw-ev-wpt-tx — UART5 U54 보드먹스 근본원인 확정·실보드 검증

- **확정 사실**: U54(SN74CB3Q3257) SEL=L→UART(B1), OE#=L→인에이블(SCDS135E Table 6-1). TCA6416 P00/P14=LOW → UART5 헤더 연결. J1.4=GPIO73=UART5_TXD, J1.3=GPIO74=UART5_RXD(post-mux, UG :1525-1526).
- **실보드 PASS (2026-06-10)**: J1.4↔J1.3 루프백 + TCA6416 P00/P14=LOW → TX==RX Logic2 토글. 세팅 전 무토글·후 토글 인과 확증.
- **2026-06-09 오진 정정**: "UART_write 주석·DE 미구현이 원인" → 오진. 실제 근본원인 = ② 보드먹스(U54+TCA6416). ① force_io(SoC PADCONFIG)는 처음부터 정상. 2층 모델([[am263p_iomux_force_io_enable]]) 추가.
- **함정 추가**: TCA6416 출력 레지스터 리셋 디폴트=HIGH → LOW 먼저 쓰고 방향 출력으로 세팅(글리치 방지). I2C1 핀: SCL=I2C1_SCL(D7), SDA=I2C1_SDA(C8) 확정.
- **갱신**: [[lp_am263p_uart_epwm_mux]](가설→확정 재작성), [[am263p_iomux_force_io_enable]](오진 정정·2층 모델), 8kw [[status]](UART5 루프백 PASS·Phase 2 분리).
- **잔여(Phase 2)**: 8kw 보드 결합 시 THVD1400 U13 DE(`EN_485`=GPIO91=J5.48) 구현.

## [2026-06-10] ingest | oled_tv_software — 02_RX_ble 모듈 분리 리팩토링 설계 결정 환원

- **작업**: `02_RX_ble` 단일 `Application/main.c`(618줄) → 관심사별 모듈 분리. 01_RX_control `app_*.c/.h` layering을 기준 삼아 순수 코드 이동(동작 불변 목표). 빌드: `emBuild` 에러 0·경고 0, `RX_BLE.hex` 산출. 실보드 검증 미수행(내일 예정).
- **디렉토리**: `Application/Inc/app_*.h` + `Application/Src/app_*.c`, `main.c`는 루트 잔류.
- **모듈 분할**: `app_gpio`/`app_clock`/`app_uart`/`app_spi`/`app_esb`(저수준 드라이버) + `app_protocol`(두꺼운 응용 계층: SPI exchange·ESB ACK forwarding·comm_st 판정·monitor, `protocol_loop()` 단일 진입점). 계층 방향 단방향 정리(esb_pkt[] = app_esb 소유, SPI 버퍼·comm_st = app_protocol 소유).
- **`_shared` 변경**: `pkt_checksum` static → 공개 함수로 승격. 02 자체 `calc_checksum` 제거. 01 미접촉.
- **미해결 2항목 (내일 결정)**: ① `app_uart_drv.h` 헤더명 최종 결정(nRF5 SDK `app_uart.h` shadow 회피책), ② `ADD_SPI` 매크로 전역 전파(`.emProject` `c_preprocessor_definitions` 이동) 적절성 확인.
- **신규 페이지**: [[ses_build_conventions]] (SES 빌드 함정 3개 정리).
- **갱신**: [[app_protocol_module]](3펌웨어 표준 패턴·모듈 분할·계층 방향·`_shared` 체크섬 API 절 추가), [[status]](다음 시작점·02 리팩토링 행·미결 2항목), [[roadmap]](§3 별트랙), [[roadmaps/spi-esb-refactor]](§3 현재 위치), index, log.

## [2026-06-10] ingest | lp-am263p — TI PROC171A 회로도 UART5 먹스 블록 (Tier 2) + THVD1400 오귀속 정정

- **소스**: TI LP-AM263P 회로도 SPRR503A(`PROC171A`, Rev A). [[schematic_ingest_strategy]] **Tier 2**(PDF 텍스트레이어) — Altium `.SchDoc`이 바이너리 OLE라 Tier 1 네트리스트 export 불가(라이선스). 동봉 SCH PDF는 `pdftotext -layout` 추출 양호. raw `teams/g/lp-am263p/raw/proc171_schematic/`(PDF 전체 + 시트 11/13/21/23 텍스트). 새 소스 [[schematic_lp_am263p]].
- **정정(검증된 오류)**: wiki가 RS-485 트랜시버 **THVD1400 U13을 lp-am263p 부품**처럼 다뤘으나 오류. 네트리스트에 `485`/`THVD`/`RS485` 0건 → **LP-AM263P엔 RS-485 트랜시버 없음**. THVD1400 U13은 **8kw-ev-wpt-tx 커스텀 보드** 부품(LP를 모듈로 결합). J5.48=GPIO91은 LP↔8kw 경계 핀. 수정: [[am263p_iomux_force_io_enable]] :87/:91, [[am263p_syscfg_soft_vs_hard_assign]] :49.
- **핵심 발견 → [[lp_am263p_uart_epwm_mux]]**: UART5_TXD/RXD는 온보드 **U54(SN74CB3Q3257) FET 버스스위치**로 EPWM9와 다중화돼 BP 헤더(`EPWM15_A/B_BP`)로 나감. 먹스 SEL(pin1)/EN(pin15, active-low)은 **TCA6416 IO expander(U63, AM263P_I2C1 @0x20)의 P00/P14**가 구동 — GPIO 아님, 제어선 풀저항 없음. TCA6416 리셋=전포트 입력 → **펌웨어 I2C 설정 전 먹스 미정**.
- **8kw 함의(가설, 미검증)**: 8kw가 BP 헤더(post-mux)에서 UART5 탭하면 LP의 이 먹스가 UART로 설정돼야 신호가 나옴 → 8kw UART5 미동작의 **LP-측 제3 후보 원인**([[am263p_iomux_force_io_enable]] 펌웨어 IOMUX 원인배제 + UART_write 주석 + RS-485 DE 미구현 위에 추가). 검증: 펌웨어 TCA6416 설정 grep + JTAG expander 레지스터 read + 헤더핀 스코프.
- **확인 필요**: BP 헤더 J-핀 정합(회로도 net 핀34/J7.45 vs UG J1.4/J1.3), J1.4 post/pre-mux 여부, SEL 극성, 누가 expander 디폴트 설정(TI Board init?).

## [2026-06-10] ingest | oled_tv_software — UART monitor 텍스트→바이너리 전환 + PC GUI 추가 (commit 35b94d0)

- **근거 커밋**: `35b94d0` (branch esb, 2026-06-10 실보드 검증). 직전 `2f2aa65`(COMM 라인 2인자·이벤트화) 위에, 01_RX_control UART5 모니터를 **텍스트 printf → 11B 바이너리 패킷 송출**로 바꾸고 host PC GUI(`tools/pc_uart_gui/uart_gui.py`)를 추가.
- **monitor 바이너리화**: `print_packets()`가 6헤더(0x10/0x11/0x12/0x50/0x51/0x52)를 `pkt_build_tx`/`pkt_build_rx`로 빌드해 신규 `uart_send()`(app_usart)로 1초 주기 송출. wire 11B(`[HDR][LEN=0x08][DATA[8]][CRC]`, BE, scale 0.01) 불변 — 이제 UART에도 흐름. TeraTerm으로 열면 깨져 보이는 게 정상.
- **COMM 텍스트 라인 폐기**: `print_comm_line_on_change()` 삭제. 링크 health(SPI_Comm_St/BLE_Comm_St)는 0x10 status d0 **bit5/bit6**로 운반(1초 주기 항상 실림) — 별도 이벤트 라인 불필요. `pkt_print_comm_line()` 공유 포매터는 호출처 없는 orphan.
- **PC UART GUI(신규)**: Python+Tkinter+pyserial. 단일 UART5 송수신, 11B HDR 동기+CRC(`pkt_checksum` XOR 포팅) 재동기(1바이트 슬라이드 → command 텍스트 잡음 자연 폐기). 2컬럼(좌 TX 0x10~12/우 RX 0x50~52) 뷰·필드명 사전표기·값만 갱신. `Link: SPI [UP/DOWN] ESB [UP/DOWN/-]`(d0 bit5/6). buck 입력칸 2개→`buck <v>\r` 송신, 확인은 0x51 `Tx_Buck_Vout_Ref`(volts×100).
- **buck 경로 불변**: end-to-end(UART→0x51 DATA[6,7]→SPI→ESB→03)는 그대로, 확인 방법만 텍스트→바이너리 0x51 파싱으로.
- **무변경**: command 채널(UART5 라인 단위 ISR 파싱)·응답 printf(`buck=.. V`)는 수동 TeraTerm 디버그용으로 잔존. command 응답 텍스트와 바이너리 모니터가 한 포트에 섞여 나감.
- **빌드 함정(신규 페이지)**: STM32CubeIDE CLI 빌드 불가(`stm32cubeidec.exe` GUI 서브시스템·즉종료) → IDE Ctrl+B. CubeMX 재생성 금지. [[cubeide_cli_build_trap]].
- **로드맵**: [[roadmaps/pc-gui]] G0~G3 완료(G0 결정=UART5 단일 포트·monitor 바이너리 전환).
- **신규 페이지**: [[pc_uart_gui]], [[cubeide_cli_build_trap]].
- **갱신**: [[comm_state_monitoring]](갱신이력3·monitor 바이너리 전환 절·pkt_print_comm_line historical 강등·보류·관련), [[app_protocol_module]](print_packets 바이너리화·print_comm_line_on_change 삭제·빌드함정·관련), [[spi_link_reliability]](링크표시 행·LINK DOWN/UP·단절후속), [[rx_control]](메인루프·UART5절), [[spi_packet_format]](11B가 UART에도), [[uart_command_set]](방향 주의), [[buck_vout_ref_command_path]](확인방법), [[status]](다음시작점·현황표 행3개·미결·예정), [[roadmap]](§3·§5·date), index, log.
- ⚠️ **직전 환원(2f2aa65 COMM 라인 이벤트화, commit 66e1892)의 'COMM 텍스트 라인' 기술은 이번에 historical 강등** — `35b94d0`이 그 텍스트 라인 자체를 제거했기 때문.

## [2026-06-10] ingest | 8kw-ev-wpt-tx — PWM 주파수 85kHz 고정 + dead-time config 분리 구현·실보드 검증 (commit d01fc0a)

- **근거 커밋**: `d01fc0a` (branch pwm). 직전 `8046744`(dead-time 단일소스)·`6e6b342`(P1 4핀) 위에 **주파수 확정값(85 kHz) 반영 + 튜닝 knob 파일 분리**를 얹어 4채널 실측 PASS. P2 △→✓.
- **주파수 85 kHz 고정·실측**(전엔 "확정 스펙"일 뿐 미구현): `TBPRD 1000→1176`, `cmpA 500→588`, `EPWM7 CMPB 470→558`(@150 ns). Saleae **85.032 kHz**(+0.002%, 주기 11.7603 µs, 지터 σ≈0.74 ns) — 계산 1176과 일치. **TBCLK=200 MHz는 이제 전제 아닌 확정 사실**(1 count=5 ns).
- **dead-time 단일소스 위치 이전**: ~~`eta_pwm.h ETA_DEADTIME_NS`~~ → **`src/eta_bsp/eta_tuning.h`**(신설, HW 엔지니어용 컴파일타임 knob 전용). **유효범위 100~400 ns, 이탈 시 `#error` 빌드 차단**. 한 줄만 바꿔 재빌드→파생값(COUNTS·EPWM7 CMPB) 자동 추종.
- **런타임 override → SysConfig 면역**: 주파수(TBPRD/cmpA)·dead-time 모두 `eta_pwm_init()`이 런타임 override → `example.syscfg` 재생성으로 기본값 덮여도 면역. `example.syscfg`는 안 건드림. ⚠️ **빌드 환경**: CCS makefile이 절대경로 박음 → 다른 노트북 clone 후엔 CCS import로 재생성해 빌드. `eta_tuning.h`는 순수 C 컴파일이라 syscfg 재생성 불요(override 방식 이점).
- **검증(Saleae 4ch: HS1 J4.39/LS1 J4.40/HS2 J6.52/LS2 J6.51, dead-time 100/150/400 ns 스윕, 전 주기)**: duty(HS) 49.15/48.73/46.60% — `50%−dt/T` 정확 추종(AHC 정상, 결함 아님); dead-time 100/150/400 ns 완벽 선형(20/30/80 counts, 레그1 σ<1 ns); **shoot-through 양 레그 전 주기 0건**(최소 DT 89 ns 양수 마진). **PASS.**
- **새 사실 — 레그2 dead-time 비대칭(향후 P3/P4 마진)**: 두 모듈 동기라 모듈간 **~11 ns(≈2.2 counts) 고정 위상 스큐** → dead-time HS→LS +11/LS→HS −11 ns 비대칭(합=2×설정). 레그1(단일 모듈 dead-band)은 없음. 현 스펙(100~400 ns) 무해(89 ns 마진), **50 ns 이하 시 마진 재확인**, 대칭 필요 시 EPWM7 CMPB +2 counts 트림. → 플랫폼 일반 사실로 [[am263p_epwm_module_sync_deadtime]] §함정에 승격.
- **dead-time 최종값은 미결 유지**: 현재 150 ns 베이스라인 커밋, 전력단 브링업 때 100~400 ns 중 확정. (인프라·config 분리는 완료.)
- **갱신**: [[status]](소스레이아웃 eta_pwm/eta_tuning.h·§85kHz 검증절·현황표·미결[비대칭·빌드환경·최종값]·다음), [[pwm]](§1 사실·§2 P0/P2 표·§3 dead-time 단일소스 위치·§85kHz 검증절·§레그2 비대칭절·§빌드 환경절·§4/5/6·date), [[pwm_pinmap]](스펙 85.032kHz·단일소스 위치·비대칭), [[am263p_epwm_module_sync_deadtime]](§함정 위상스큐 비대칭·§검증 85kHz·§8kw 인스턴스 CMPB558/eta_tuning.h), [[roadmap]](pwm 행 P2✓·현재위치), log·index.

## [2026-06-10] ingest | 8kw-ev-wpt-tx — 레그2 SYNC dead-time concept 승격 + 주파수 85kHz 고정 확정·dead-time 100~400ns

- **concept 승격(신규)**: [[am263p_epwm_module_sync_deadtime]] (lp-am263p 플랫폼 concept — 선례 [[am263p_epwm_primary_pad_no_force_io]]와 동일 배치). 풀브리지 레그 HS/LS가 다른 EPWM 모듈에 걸칠 때: master `syncout=ON_CNTR_ZERO`→slave `syncin`·phaseShift=0 위상정렬 + slave AQ 반전 + CMPB 오프셋(`TBPRD/2−DT`, `<TBPRD/2` 엄수). SYNC-in 기본 disable(자유구동) 주의·dead-band 레그와 ns 소스 공유. 8kw 레그2(EPWM4_A→EPWM7_B) 실측 출처. [[pwm]] §3 환원 후보 해소(승격 완료).
- **주파수 확정(사용자 2026-06-10)**: 브링업 임시 100 kHz → **85 kHz 고정**. UP_DOWN `TBPRD=TBCLK/(2·f)=200MHz/(2·85kHz)≈1176`[정수·실측은 코드 확인]. dead-time 카운트는 TBCLK 기준이라 주파수 무관, CMPB의 `TBPRD/2`만 재계산.
- **dead-time 범위 확정**: **100~400 ns 조정 가능, 실험 후 고정 예정**(기존 "시작 150ns" → 범위 명시). 100ns→20·400ns→80 count(5ns 배수라 절삭손실 0). 검증 빌드(150/300ns)는 브링업 100kHz에서 수행 — 85kHz 재빌드 시 결론 동일.
- **갱신**: [[am263p_epwm_module_sync_deadtime]](신규), [[pwm]](주파수·dead-time범위·concept 링크·검증 100kHz 맥락·P0/모름/블로커/환원후보·date), [[pwm_pinmap]](스펙 85kHz·dead-time범위·concept 링크·date), [[status]](스펙·미결·다음·date), [[team_briefing_8kw]](로드맵 P0/P2·스펙·§5·date), [[roadmap]](pwm 행·현재위치·date), index(concept 신규 + pwm·pwm_pinmap 줄).

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM dead-time 단일소스 #define 통일(두 레그·두 메커니즘·하나의 ns 소스) + 스윕 검증 (commit 8046744)

- **근거 커밋**: `8046744` (branch pwm). dead-time을 두 레그 모두 `eta_pwm.h` `#define ETA_DEADTIME_NS` 하나로 통일 + 150/300ns 스윕 4채널 실측. (직전 P1 4핀 = `6e6b342`.)
- **사실관계 정정**: 직전 wiki는 "레그1 dead-time 단일소스 미적용 — 향후 통일 예정"으로 적었으나, `8046744`가 **레그1까지 통일 완료** → [[pwm]]·[[status]] 해당 후속 항목 해소.
- **단일소스 패턴(핵심)**: `ETA_DEADTIME_NS`(=150U) → `ETA_NS_TO_COUNTS(ns)=(uint16_t)((uint32_t)ns*(TBCLK_HZ/1MHz)/1000)` 정수 floor. **TBCLK=200MHz → 1 count=5ns**, 150→30·300→60(절삭손실 0), TBPRD=1000(UP_DOWN 100kHz). `ETA_DEADTIME_COUNTS=30@150ns`.
  - **레그1(EPWM2 dead-band)**: `eta_pwm_init()`이 `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`로 RED/FED=ETA_DEADTIME_COUNTS 재적용(RED=FED 대칭, 주기당 갭 2개, SysConfig 기본 override).
  - **레그2(EPWM7 CMPB 오프셋)**: `ETA_EPWM7_CMPB_INIT=TBPRD/2−ETA_DEADTIME_COUNTS`(=470@150ns) → `EPWM_setCounterCompareValue(...COMPARE_B...)`. **CMPB<TBPRD/2 엄수**(초과 시 shoot-through).
  - 요지: **메커니즘 둘(dead-band RED/FED vs CMPB 오프셋)·ns 소스 하나**, build-per-change(숫자만 바꿔 재빌드).
- **검증 방법(환원)**: flash 없이 RAM-load(OCRAM)→run + Saleae Logic2 4ch, **500MS/s(2ns 격자)**, **transition-based CSV export**(오프라인 수치분석 유리). dead-time=상보쌍 both-LOW 갭, shoot-through=both-HIGH 겹침. 샘플레이트=타임스탬프 격자 GCD 추정.
- **검증 결과(150·300ns 두 빌드)**: 4ch 100kHz±0.1% 상보 유지; dead-time 레그1 150.3→300.4ns(1.998×)·레그2 150.0→300.0ns(2.000×); **shoot-through 0**(양 빌드·양 레그); 레그1 RED=FED 대칭 확인. ⚠️ **+0.3ns 초과는 2ns 격자 양자화 바이어스**(floor 절삭/타이밍 오차 아님 — 30·60 정수라 절삭손실 0).
- **wiki 정합 메모**: 작업 지시는 "[[pwm]]/[[status]] dangling, 신설"이었으나 **디스크 확인 결과 둘 다 실존**(`roadmaps/pwm.md`·`status.md`, Obsidian이 파일명으로 해석) — 신설 아닌 기존 §dead-time 단일소스 절 확장으로 처리. P2도 △로 진척 반영.
- **갱신**: [[pwm]](§dead-time 단일소스 절 매크로·양 레그·검증표 확장, §검증 방법·결과 신설, P2 △·마일스톤·현재위치·사실·환원후보), [[status]](후속 해소·현황표·다음), [[pwm_pinmap]](dead-time 두 경로 단일소스 수렴 1줄), [[team_briefing_8kw]](로드맵 P1✓/P2△·보고포인트·§5), [[roadmap]](pwm 행), index.

## [2026-06-09] ingest | oled_tv_software — 패킷 크기 정정(54/43) + app_protocol 적출 + 정리트랙 추월 (esb 9be1a7a)

근거: c-oled_tv_software repo 코드 `9be1a7a`(esb). 코드 직접 확인 후 환원. 네 갈래:

1. **패킷 크기 사실 정정**: 내부 데이터 컨테이너 `rx_module_data_t`/`tx_module_data_t` 크기를 코드 static_assert(`_shared/oled_tv_protocol.h:237-238`) 기준 **rx 54B / tx 43B**로 정정. wiki에 62B/51B(canonical [[spi_packet_format]])·56B/45B(entity·source) 두 드리프트값 혼재 → 모두 코드값으로. wire는 불변 11B. 갱신: [[spi_packet_format]]·[[rx_control]]·[[rx_ble_module]]·[[esb_ptx_ack_assembly]]. (entity 교차참조의 "HDR 0xC0·20ms"도 정정 — 실제 HDR 0x10–12/0x50–52·10ms.) **코드 repo `CLAUDE.md:20`도 45B/56B로 낡음 → 별도 갱신 필요(메모, wiki 밖).** source 스냅샷(prd/manual/schematic)은 historical로 잔존, static_assert가 정본.
2. **정리트랙(spi-esb-refactor) 코드 추월**: R1~R3 부분 구현(공유 `_shared/oled_tv_protocol.{c,h}`+`pkt_build_*`/`pkt_apply_*`/`pkt_print_*`), R4(`SPI_PKT_*` 개명) 무효 — 코드는 이미 링크 중립 `PKT_HDR_*`. [[roadmaps/spi-esb-refactor]] 표·§5 갱신, [[roadmap]] §5·[[status]] 반영.
3. **새 트랙 — app_protocol 적출/핸드오프 (완료·검증)**: 01의 SPI 프로토콜을 `common.c/h`→`app_protocol.c/h`로 적출. 공개 API `protocol_loop()` 하나(내부 static `exchange_packets`/`print_packets`) + 전역 3개. 4파일 자립(common.h 역의존 끊음). W1=트랜스포트 직접 호출, D1=센싱/지령 전역 유지(비-SPI 호출처 무수정). 더미 한 줄 토글·모니터 상시 ON·LINK UP/DOWN 출력 제거(COMM 중복)·죽은코드(monitor_spi_diag/spi_ok_cnt/build_rx_to_tx_pkt/LOG_EN/tx_data_log) 삭제. main 루프 = `adc_proc()`+`protocol_loop()`. **STM32CubeIDE 실 빌드 + 실보드 동작확인 완료(✓).** 신규 [[app_protocol_module]], [[rx_control]] 메인루프 갱신, [[status]] 반영, Monitor_Loop(`175a8f7`) 주석 미결 해소.
4. **남은 후속(미착수)**: `_shared` 매크로 소유권 점검 — `PACKET_INTERVAL`(10ms)은 01만 호출(02/03 ESB 1ms 미사용)이라 SPI 전용 분리/개명(`SPI_PACKET_INTERVAL_MS`) 후보. [[roadmaps/spi-esb-refactor]] §6. (esb_crc=-1은 의도된 설계로 확정 — 점검 대상 아님.)

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM P1 완료(4핀) + 레그2 두 모듈 SYNC 상보 설계 + dead-time 단일소스 #define

- **근거 커밋**: `6e6b342` (branch pwm). P1 = PWM 4핀(HS1/LS1/HS2/LS2) 전부 실보드 검증 완료.
- **LS2 = EPWM7_B @ J6.51 확정**: 이전 "핀 미확정"을 해소. UG Table 2-30(`ug:1640`) Mode0=EPWM7_B 일치(오기 없음) + **pinmux.csv 핀 F1=EPWM7_B 교차확인**. 펌웨어 배정 정본=silicon 채널.
- **회로도 net 라벨 함정 정확화**: 회사 회로도가 레그2 net을 채널이름 스타일 "EPWM4_B"(HS2)/"EPWM7_A"(LS2)로 라벨링 — 이 **suffix가 핀 노출 silicon 채널과 반대**(실제 EPWM4_A/EPWM7_B). HS2·LS2 동일 패턴. **정본=silicon 채널**, 라벨 suffix에 끌려가지 말 것([[adc_pinmap]] l/I 오기 동류).
- **레그2 두 모듈 SYNC 상보 설계(SDK 1:1 예제 없던 자리, 해결)**: EPWM4 syncout(ON_CNTR_ZERO)→EPWM7 syncin·phaseShift=0 위상정렬 + EPWM7_B AQ 반전 + CMPB 오프셋으로 상보+dead-time(레그1 dead-band 대신 CMP 오프셋). ⚠️ **함정: `CMPB=TBPRD/2−DT_COUNTS`(반드시 <TBPRD/2). +부호면 LS ON이 HS OFF 넘어 shoot-through** — 구현 중 1회 부호 오류 잡음.
- **dead-time 단일소스 #define 패턴(신규)**: `eta_pwm.h` `ETA_DEADTIME_NS` → `eta_pwm_init()`이 CMPB에 1회 적용, build-per-change(150↔300ns 실측). 레그2 적용, **레그1(EPWM2 dead-band) 미적용 → 향후 통일**(별도 세션).
- **게이트 극성**: active-high 가정으로 4핀 검증 통과(상보·dead-time·shoot-through 0) → **가정 실보드 실증, 회로도 원본 미확인**.
- **검증 실측치**: 100kHz, HS2 50%/LS2 47%, dead-time 150ns 양 edge, shoot-through 0 (Saleae 125MS/s, 13,421주기 전수 스캔). HS1 별도 99.997kHz/50%.
- **갱신**: [[pwm_pinmap]](표 4핀 확정·회로도 라벨 함정·LS2 EPWM7_B·게이트극성·SYNC 요약), [[pwm]](P1 ✓완료·Pin4 SYNC 설계절·dead-time 단일소스절·P2 레그1 통일잔여·블로커 해소·환원후보), [[status]](P1 완료·현황표·미결 재구성), index 2행.

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM 핀맵 net/채널 분리 정정 + Pin3 HS2 실보드 검증 + EPWM 인스턴스·자유구동 사실

- **정정 대상**: [[pwm_pinmap]] "사용자 net 라벨" 컬럼이 **보드 net과 SoC 채널을 혼동**. J6.52 행을 "EPWM4_B"로 적었으나 — ① UG가 강제하는 SoC 채널은 **EPWM4_A**(Mode0/primary, `teams/g/lp-am263p/raw/lp_am263p_ug/ug_lp-am263p.md:1641`), ② J6.52에 라우팅된 **보드 net은 PWM_HS2**(레그2 HS 게이트, 사용자 도메인 확인). 펌웨어도 EPWM4_A hard `$assign`으로 실측 통과.
- **정정 방향**: 표를 **3단 모델(커넥터 핀 → SoC 채널 UG Mode0 → 보드 net)** 로 재구성, "EPWM4_B/EPWM7_A" 표기 제거. 이전 [2026-06-09 decision]의 "net 라벨 _B/_A vs 채널 반대" 프레이밍 자체가 net과 채널 혼동이었음 → 정정(net=PWM_HS2/LS2, 채널은 핀이 강제).
- **UG 교차확인**: J4.39=EPWM2_A(`:1600`), J4.40=EPWM2_B(`:1601`), J6.52=EPWM4_A(`:1641`), J6.51=EPWM7_B(Mode0)/EPWM5_B(Mode10)(`:1640`). 레그1·HS2는 UG·실측 정합.
- **Pin3 HS2 검증 환원**: EPWM4_A@J6.52 펌웨어 구현·실측 **99.998kHz/50%** → P1 진행 **1/4→2/4**(Pin1·Pin3 ✓, Pin2 LS1·Pin4 LS2 남음).
- **신규 reference 사실(검증 근거)**: ① **EPWM4는 EPWM2와 독립 인스턴스**(SysConfig 수용, base `CSL_CONTROLSS_G0_EPWM4_U_BASE`). ② **SysConfig 기본 EPWM = SYNC-in disable + phaseShift=0 → 자유구동** → 단일 모듈 핀은 위상기준 없이 독립 검증 가능(HS2 레그1 무관 토글 실증). 단 레그2 상보·dead-time(Pin4)은 EPWM4↔EPWM7 SYNC 명시 활성화 필요.
- **LS2 핀 미확정 명시**: 레그2 LS2는 **EPWM7 모듈만 사용자 확정**, 커넥터 핀 미확정 → J6.51은 "EPWM7 노출 UG 후보 핀"으로만 기재(검증된 사실 아님). Pin4 착수 시 호명.
- **갱신**: [[pwm_pinmap]](표 3단 재구성·net/채널 정정·EPWM 인스턴스 자유구동 절 신설·LS2 핀 미확정·source), [[status]](Pin3 검증·P1 2/4·미결 2항), [[pwm]](P1 표·Pin3/4 행·현재위치), index 2행.

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM P1 Pin1(HS1) 구현·실보드 검증 + EPWM primary 패드 force_io 불요 정본

- **출처**: PWM P1 Pin1 = EPWM2_A → J4.39 (PWM_HS1) 실보드 검증.
- **검증 실측(Saleae Logic2)**: **99.997 kHz / duty 49.998%**(n=10223 cycles), 깨끗한 토글·글리치 없음. 100 kHz는 **브링업 임시값**(확정 주파수 pending — 추정 금지).
- **핀맵 정본↔실측 불일치 없음** — EPWM2_A@J4.39(UG Mode0) 그대로 동작. [[pwm_pinmap]] HS1 행에 "검증됨" 마킹.
- **신규 정본 [[am263p_epwm_primary_pad_no_force_io]]** (lp-am263p): EPWM 출력이 핀 **primary function**이면 SysConfig 핀먹스만으로 출력 버퍼 켜짐 → **force_io_enable 불필요**. force는 alt-function 패드(UART5=EPWM15)만 — [[am263p_iomux_force_io_enable]]와 **대조 짝**. 근거=Pin1 force 없이 출력. 판별=UG 핀먹스 Mode0(primary)인지 alt인지. + **검증법 환원**: OCRAM 이미지라 flash 없이 ccs-debug `loadProgram→run` + Saleae로 핀 측정(디버그 끊겨도 RAM 이미지 계속 실행) — dead-time build-per-change 튜닝에 유리.
- **P1 진행 1/4**: Pin1 ✓. 남음 = Pin2 LS1(EPWM2_B@J4.40, 레그1 dead-band 상보) → Pin3 HS2(EPWM4_A@J6.52) → Pin4 LS2(EPWM7_B@J6.51, 레그2 SYNC+위상오프셋).
- **확인 필요(미확정)**: ① 실제 스위칭 주파수 ② 레그2 두-모듈(EPWM4+EPWM7) SYNC+위상오프셋 상보·dead-time 구체 설계 — SDK 1:1 예제 없음, Pin4 착수 시 설계.
- **갱신**: [[pwm]](P1 △1/4·핀별 표·검증법·환원 후보), [[pwm_pinmap]](HS1 검증됨), [[status]](PWM 트랙·현황표 △), [[am263p_epwm_primary_pad_no_force_io]](신규), index 2건(concept 신규·pwm 진행).

## [2026-06-09] ingest | oled_tv_software — comm-state 판정 (T,N) 상수 통일·spi_status LINK/CRC 분리·COMM 라인 환원 (esb d2232fe)

- **근거 커밋**: `d2232fe`(esb, 2026-06-09) "feat(comm): 통신상태 판정 T/N 상수 통일 + 3칩 공통 COMM 라인". 코드 직접 확인 후 환원.
- **낡은 값 정정**: `BLE_COMM_ST_MIN_COUNT` 3→**20**(200ms 윈도우 기대 ~200개의 ~10%; `ESB_TX_INTERVAL_MS=1ms`). SPI는 `SPI_COMM_ST_TIMEOUT_MS=5000`→`SPI_COMM_ST_WINDOW_MS=1000`(개명·단축). 02/03 판정 코드 `delta >= MIN_COUNT` 확인.
- **새 모델**: comm-st 임계 = percent 자동계산 폐기, **각 링크 (T,N) 직접 상수**(헤더 한 블록). SPI=rolling-timeout(01만 소비, `MIN_COUNT=1`은 직접 미참조 문서값, 02/03 unused #define), BLE=윈도우 카운트(02·03 소비).
- **spi_status LINK/CRC 분리**: 01의 `spi_status`가 LINK 전용(토글 타임아웃)으로 분리, CRC는 1초 윈도우 fail로 별도(이전 `e5e3efc` 통합을 환원). diff: `spi_proc()`에서 ok/CRC-fail 시 `spi_status` 적던 두 줄 제거.
- **3칩 공통 COMM 라인**: `pkt_print_comm_line(spi_link,spi_crc,esb_link,esb_crc)` in `_shared/oled_tv_protocol.c`. 출력 `COMM | SPI:{L}{C} ESB:{L}{C}`(1=up/ok,0=down/err,-=N/A). 함수는 칩 무지. **현재 01만 호출**(common.c:200), SPI down이면 ESB 전부 stale `--`.
- **보류·미구현 표기**: 02/03 COMM 라인 미와이어링(unused), ESB CRC는 HW CRC 보증으로 SW 검증 안 하기로 결정(자리는 `-`).
- **재확인(불변)**: race-free stamp 설계(02가 `spi_tx_pkt`에 `SPI_Loop` 송신 직전 stamp, `pkt_build_tx` extra_d0 아님) — d2232fe가 02 미수정, 기존 기록 정확.
- **갱신**: [[comm_state_monitoring]](frontmatter date·심볼표·판정식·(T,N)모델 신설·LINK/CRC분리 신설·COMM라인 신설·보류절), [[status]](다음 시작점·구현현황 2행·BLE행·미결 2항), [[roadmap]](§3·§5 후속 N=20 반영), [[spi_link_reliability]](단절판정·경고출력 LINK/CRC 분리), index.

## [2026-06-09] decision | 8kw-ev-wpt-tx — PWM 레그2 suffix UG 기준 확정 + 레그2 한 모듈 묶기 향후 요청 기억

- **사용자 결정 1 — A/B suffix는 UG 기준**: 레그2 구현 채널 = EPWM4_A@J6.52, EPWM7_B@J6.51로 확정(schematic net 라벨 _B/_A와 반대지만 핀이 강제). [[pwm_pinmap]] "확인 권장" 헤징 제거 → 확정.
- **사용자 결정 2 — 레그2 두 모듈은 의도된 현 설계, 단 향후 수정**: 현 회사 회로도가 레그2(HS2/LS2)를 EPWM4+EPWM7 두 모듈에 라우팅한 것은 의도적. **사용자가 회로도 수정 요청 기회가 생기면 한 EPWM 모듈로 묶도록 요청할 계획** → 그때 상기시킬 것.
- **기억 저장**: 영구 메모리 `project_8kw_pwm_leg2_revision.md`(project type) 신규 + MEMORY.md 포인터. wiki [[pwm_pinmap]] §향후 보드 개선 + [[pwm]] §6 환원/개선 후보에도 기록.
- **갱신**: [[pwm_pinmap]](§핵심·§향후 보드 개선·§미확인), [[pwm]](§5·§6), [[status]](미결 reframe), [[team_briefing_8kw]]. PWM 상태 = 핀맵 확정·P1 착수 대기(불변).

## [2026-06-09] resolve | 8kw-ev-wpt-tx — PWM 핀맵 확정 (J4.38→J4.39 정정 + UG 교차확인) → P1 착수 가능

- **사용자 정정**: J4.38은 오기, 실제 **J4.39**(EPWM2_A=PWM_HS1). → 레그1이 UG와 완전 일치(EPWM2_A@J4.39, EPWM2_B@J4.40)하며 **UG 표 신뢰성 검증**.
- **확정 핀맵([[pwm_pinmap]])**:
  - 레그1 = **EPWM2 단일 모듈**: EPWM2_A=HS1@J4.39, EPWM2_B=LS1@J4.40.
  - 레그2 = **EPWM4+EPWM7 두 모듈**: EPWM4_A=HS2@J6.52, EPWM7_B=LS2@J6.51.
- **A/B suffix 정리**: 레그2에서 사용자 net 라벨(_B/_A)과 silicon 노출 채널(_A/_B)이 반대. 물리 핀이 노출하는 채널은 J6.52=EPWM4_A뿐·J6.51=EPWM7_B(Mode0)뿐이라, **구현 기준은 UG 채널**(EPWM4_A@J6.52, EPWM7_B@J6.51). net 이름에 끌려가지 말 것.
- ★ **레그2 두 모듈 함의**: J6.51이 EPWM4_B를 노출 안 해 한 모듈로 못 묶음 → 레그2 상보·dead-time은 모듈 내 dead-band 불가, **EPWM 동기(SYNC)+위상 오프셋**으로 생성(레그1 단일모듈 dead-band와 비대칭). dead-time 튜닝 경로도 레그1=레지스터/레그2=오프셋으로 다름. 비표준이라 설계 의도 재확인 권장(보드 라우팅은 고정).
- **인스턴스 3개**: EPWM2/4/7. UART5(EPWM15) 무충돌.
- **상태 변화**: 직전 correction(핀맵 UG 불일치·P1 차단) → **해소**. 핀맵·토폴로지·dead-time(150ns build-per-change) 확정 → **P0 대부분 해소, 다음 착수 = P1**. 잔여 = 주파수 확정값·보호신호.
- **갱신**: [[pwm_pinmap]](확정 표·레그2 두모듈 함의), [[pwm]](§0·§1·§2·§3·§5 P1 착수), [[status]](PWM 트랙 P1·현황표·미결), [[team_briefing_8kw]](다이어그램·다음주 보고=P1), index 2건.

## [2026-06-09] correction | 8kw-ev-wpt-tx — PWM 핀맵, UG 교차확인서 불일치 발견 → "확정" 철회·확인 필요

- **정정 대상**: 직전 PWM 핀맵 "확정" entry. **UG 핀먹스 표([[lp_am263p_ug]] Table 2-28 J4 / 2-30 J6) 교차확인 결과, 사용자 제공 4핀 중 3핀 불일치** → 정본 [[pwm_pinmap]]을 "확인 필요"로 다운그레이드.
- **사용자 정정 입력**: J6.51 = **EPWM7_A** (직전 EPWM&_A 오타 → 내가 EPWM4_A로 잠정기입한 것 정정).
- **UG 교차확인 결과**:
  - J4.38: 사용자=EPWM2_A인데 **UG는 EPWM1_B(Mode0)/EPWM4_B(Mode10)** — EPWM2_A는 UG상 **J4.39**(off-by-one 의심).
  - J4.40: 사용자=EPWM2_B, **UG=EPWM2_B ✅ 유일 일치.**
  - J6.52: 사용자=EPWM4_B인데 **UG=EPWM4_A**(J6.52엔 _B 없음).
  - J6.51: 사용자=EPWM7_A인데 **UG=EPWM7_B(Mode0)/EPWM5_B(Mode10)**(J6.51엔 _A 없음).
- **UG-consistent 가설 reading(미확정)**: HS1=EPWM2_A@J4.39, LS1=EPWM2_B@J4.40, HS2=EPWM4_A@J6.52, LS2=EPWM7_B@J6.51. → 이 경우 **레그2가 EPWM4(HS)+EPWM7(LS) 서로 다른 모듈**에 걸쳐 모듈 내 dead-band 불가, 동기체인+위상으로 dead-time 생성 필요(레그1 EPWM2 단일모듈과 비대칭). 인스턴스 2개(EPWM2/4)→**3개(EPWM2/4/7)** 가능성.
- **조치**: [[pwm_pinmap]]에 reconcile 표(사용자 vs UG Mode0/Mode10) + 확인 필요 명시. [[pwm]]·[[status]]·[[team_briefing_8kw]]·index에서 "핀맵 확정→P1 착수"를 "핀맵 reconcile 선결→그 후 P1"로 정정. 게이트 구동 핀이라 확정 전 SysConfig 배정 금지.
- **확정 스펙(불변)**: 풀브리지 4채널·주파수 고정형(값 미정)·dead-time만 가변(build-per-change, 시작 150ns)·UART5(EPWM15) 무충돌·P4서 ADC 트리거 RTI→EPWM 전환.
- **사용자 호명 필요**: 핀번호 off-by-one(J4.38↔39)인지 / A·B suffix 표기 혼동인지 / 다른 핀 넘버링 기준인지 reconcile.

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM 핀맵·스펙 확정 (사용자 제공) → P0 대부분 해소, P1 착수 대기

- **출처**: 사용자 제공 PWM 핀맵·스펙 (2026-06-09).
- **신규 [[pwm_pinmap]]**: 풀브리지 인버터 4채널 — J4.38 EPWM2_A=PWM_HS1, J4.40 EPWM2_B=PWM_LS1, J6.51 EPWM4_A=PWM_LS2, J6.52 EPWM4_B=PWM_HS2. **EPWM2=레그1, EPWM4=레그2.** ⚠️ **A/B↔HS/LS 매핑이 인스턴스별 반전**(EPWM2 A=HS, EPWM4 A=LS) → 레그별 상보 극성·dead-time 다르게 설정. ✅ **UART5(EPWM15) 무충돌**(이전 P0 선결 충돌 점검 해소).
- **스펙**: 스위칭 주파수 **고정형**(값 미정·런타임 가변 아님). **dead-time만 가변** — 리얼타임 변경 불필요, **값 바꿀 때마다 새 빌드(build-per-change)**, **시작 ≈150ns**. duty 등 기타 미정.
- **ADC 트리거 향후 계획**: 현재 ADC=RTI1 트리거 유지. **PWM 완료 후 ADC SOC 트리거를 RTI→EPWM으로 전환 예정**(P4). 전력제어 표준(PWM 주기 특정 시점 샘플). 지금은 RTI 그대로.
- **사실/가설/모름 갱신**: 토폴로지·채널·핀·dead-time 방식·UART5 무충돌 = **사실 승격**. LCC 탱크 = 가설 유지. 주파수 확정값·보호신호 소스·게이트 극성 = 모름(P0 잔여, 단 주파수 고정형이라 P1은 임시값 진행 가능).
- **갱신**: [[pwm]](§1 사실/가설/모름·§2 마일스톤 P0 △/P1 다음착수·§3 단계·§5 블로커), [[status]](PWM 트랙 P1 착수·현황표·미결), [[team_briefing_8kw]](PWM 다이어그램·확정 스펙·다음주 보고 포인트=P1), index 2건(pwm.md 갱신·pwm_pinmap 신규). **다음 착수 = P1**(EPWM2/4 4채널 기본 출력, dead-time 150ns, 오실로 검증).

## [2026-06-09] plan | 8kw-ev-wpt-tx — PWM 전력제어 작업 호(P0~P4) 신규 등록 (미착수)

- **계기**: ADC 계측(A2) 완료 후 다음 작업으로 PWM 구현 추가 지시. roadmap.md가 예고한 후속 작업(PWM)을 정식 작업 호로 승격.
- **신규 [[pwm]](roadmaps/pwm.md)**: P0(요구사항·핀맵 확정)~P4(ADC 피드백 제어루프) spine. 전부 미착수(✗). **사실/가설/모름 가름** 명시 — 사실(AM263P EPWM 보유, UART5가 EPWM15 점유 중), 가설(LCC 공진형 토폴로지·~85kHz SAE J2954, ADC `I_LCC_SEN` 단서), 모름(인버터 구조·채널 수·주파수·dead-time·위상·보호신호 = P0 스펙 입수 필요). 추측으로 채우지 않고 "확정 필요"로 남김.
- **P0 핵심 선결**: ① 토폴로지·채널·주파수·dead-time·보호신호 스펙 입수 ② **EPWM15(UART5 점유)와 PWM 채널 핀 충돌 회피** ③ 물리 인스턴스/핀 처음부터 hard `$assign`(ADC soft 재셔플 함정 회피).
- **갱신**: [[roadmap]](task 표 pwm 행 추가·현재 위치 "다음 활성 트랙=PWM"), [[status]](다음 작업 PWM 트랙 선두 배치·현황표 PWM 행·미결 P0 스펙), [[team_briefing_8kw]](작업 호 다이어그램 PWM·다음 작업·다음주 보고 포인트 PWM 착수), index 1행 추가. 외부 업무보고(`eta/업무보고_2026-06-09.md`)도 PWM 다음 작업 반영.
- **위치**: ADC A3가 센서 스펙 대기로 막혀 있어 PWM이 다음 진행 트랙. PWM 스펙과 센서 스펙을 함께 확보하면 두 트랙 동시 해소.

## [2026-06-09] briefing | G팀 주간 업무보고 준비 — lp-am263p briefing 갱신 + 8kw briefing 신규

- **목적**: 주간 팀 보고용 참고 페이지를 다음주 diff 가능하게 정비. 외부 보고서 파일은 wiki 밖(`C:\Users\echog\eta\업무보고_2026-06-09.md`)에 작성, wiki에는 보고 준비용 briefing을 둠.
- **[[team_briefing]] 갱신(lp-am263p)**: 6/2 상태(S6 "SPI 무응답"·원인 미상)→6/9 상태(R35~R38 계측으로 MCU 마스터 정상 입증+카드 NP 전 출력핀 침묵 입증→"NP 코어 미실행" 확정, 1순위 의심=40MHz XTAL Y1 미발진 추론, R39 오실로 측정 예정)로 갱신. **"보고 스냅샷 이력" 표 신설**(주차별 위치·핵심·다음계획 + 다음주 보고 포인트). S3는 과거 해결 사례로 보존. R35 "클럭 0회=샘플링 아티팩트(12.5→125MS/s)" 문제·해결 기록.
- **[[team_briefing_8kw]] 신규(8kw)**: 동일 구조(보고 스냅샷 이력·작업호 A0~A4·진행/문제표·현재위치·다음). 6/9 = ADC 6채널 완성·실보드 검증, 만난 문제표(트리거 결선 `enableIntr0`·soft 재셔플), 막힘=A3 센서 스펙 대기·UART5 차동 미동작.
- **갱신**: index 2건(lp briefing 설명 갱신 + 8kw briefing 신규행), 두 briefing 상호 백링크.
- **다음주 보고 시작점**: 각 briefing "보고 스냅샷 이력" 표 마지막 행 + "다음주 보고 포인트"부터 이어서 작성.

## [2026-06-09] update | 8kw-ev-wpt-tx — A2 완료: 6채널 ADC 실보드 검증 + AIN hard assign + eta_adc.c 테이블 리팩토링 (c512e3b)

- **출처**: branch `adc` commit `c512e3b`(origin/adc) — 6채널 ADC 완성·실보드 검증. 같은 날 앞선 4채널 update에 이어 6/6 달성.
- **A2 완료(6/6, 실보드 검증)**: 신규 2채널 추가 = Temp_Module1(ADC2 SOC0 AIN0 J3.25, int_xbar OUT_3/IRQ149), GA_Vin(ADC3 SOC0 AIN0 J3.26, OUT_4/IRQ150). 물리 인스턴스 **5개(ADC0~ADC4)** 사용. ADC1만 SOC0+SOC1 라운드로빈(SOC1 EOC 단일 ISR 2채널 수확), 나머지 SOC0 단독. RTI1 1 kSPS 공유. 6채널 raw→mV 변환 경로 실보드 검증.
- **AIN 핀 hard `$assign` 승격 (soft 재셔플 리스크 해소)**: 직전(b8b0ad8)까지 물리 인스턴스만 hard, AIN 핀은 soft `$suggestSolution`이었음. 신규 채널 추가 시 솔버 재셔플 방지 위해 **AIN 핀까지 전부 `$assign` hard 승격** → 재생성 후 물리 배정 ADC0~4 유지(재셔플 없음) 확인. [[am263p_syscfg_soft_vs_hard_assign]] 규칙의 실증 사례.
- **리팩토링 — eta_adc.c 테이블 주도화**: 인스턴스별 ISR 5개·init 5블록·loop 5블록(차이=베이스/결과주소·IRQ·ready플래그·SOC→채널)을 → 인스턴스 테이블 `g_eta_adc_inst[]` + 공용 `eta_adc_eoc_isr()` + 인덱스 루프로 통합. **332→232줄**, 동작·핀맵·IRQ 불변. 채널 추가 = enum 1행 + 테이블 1행(`ETA_ADC_CH_COUNT` 일원화). 단 `eta_uart5.c` 출력은 채널별 `DebugP_log` 하드코딩이라 출력 라인은 수동 추가 필요.
- **미해결 유지**: ① A3 센서 스케일링 — mV→물리량 변환 스펙 미입수(블로커). ② UART5 차동 송신 — 6채널 출력은 UART0 콘솔로만, UART5 `UART_write` 주석 + RS-485 DE/485_EN(THVD1400) 미구현.
- **다음 시작점**: A3 스케일링(스펙 대기) / UART5 차동 복구 / A4 교차검증.
- **갱신**: [[status]](전면, A2 ✓), [[adc]](A2 ✓·6채널 표·리팩토링), [[adc_pinmap]](6채널·int_xbar 열·AIN hard), [[roadmap]](A2 완료), [[am263p_syscfg_soft_vs_hard_assign]](AIN hard 승격=리스크 닫음), [[am263p_adc_instance_allocation]](8kw 5인스턴스), [[am263p_adc_rti_trigger]](6채널 확장 경과), index 3건.

## [2026-06-09] update | 8kw-ev-wpt-tx — 코드 진척 반영 (단채널→4채널, UART 주기화 완료, eta_bsp 레이어, UART5 차동 여전히 미동작)

- **출처**: branch `adc` 커밋된 상태(워킹트리 clean) 코드/git/사용자 확인 delta. wiki가 2026-06-05에 머물러 있어 역산 갱신.
- **소스 레이아웃 정정**: `src/bsp/` → **`src/eta_bsp/`**(eta_ 접두 디렉토리까지). 파일 `eta_adc.{c,h}`·`eta_uart5.{c,h}`, eta_ 접두 + _loop 접미 컨벤션. eta_bsp 레이어 도입(a655de4, edddc31).
- **ADC 단채널→4채널(목표 6, 4/6)**: TEMP_MODULE2(ADC1 SOC0 AIN0 J3.24 IRQ146), I_LCC_SEN(ADC4 SOC0 AIN0 J3.27 IRQ148), I_COIL_SEN(ADC0 SOC0 AIN1 J3.28 IRQ147), GA_IIN_SEN(ADC1 SOC1 AIN1 J3.29 IRQ146 SOC1 EOC). ADC1 SOC0+SOC1 라운드로빈→SOC1 EOC 단일 ISR 2채널 수확. 트리거 RTI1(syscfg `CONFIG_RTI0`) 1 kSPS 3인스턴스 공유. ISR raw 저장, `eta_adc_loop` `(raw*3300)/4095` 정수 mV(out-param, 88d9deb). 인스턴스 hard `$assign`(b8b0ad8)이나 **AIN 핀은 아직 soft** = 잔존 리스크.
- **UART 1초 주기화 완료**: RTI2 독립 타이머(syscfg `CONFIG_RTI1`) compare0 ISR→flag→`eta_uart5_loop`(8b85bda). 주기=SysConfig `nsecPerTick0=1e9` 단일 진실원천(#define 아님). 현재 출력은 UART0 콘솔(`DebugP_log`) 4채널 ASCII.
- **UART5 차동 송신 여전히 미동작**: `snprintf`+`UART_write` 블록 통째 주석(`eta_uart5.c:159-170`) → 시도조차 안 함. RS-485 DE/485_EN(THVD1400 U13) 미구현(src `485`/`DE`/`THVD` 0건). TX force-enable(IOMUX)은 살아있음(TXD=EPWM15_A=J1.4). PADCONFIG `0x53100124` 런타임 read 미수행. → soft 재배치 점검(2026-06-09 예정분) 결론: UART5는 soft 아님 확정, 원인=UART_write+RS-485.
- **A3 블로커 유지**: 센서 스펙 미입수, mV→물리량 변환 코드 전무.
- **다음 시작점**: ① 남은 2채널(Temp_Module1 J3.25 ADC2, GA_Vin J3.26 ADC3) → 6채널 ② AIN 핀 hard `$assign` 검토 ③ UART5 차동 복구(UART_write 주석 해제+RS-485 DE 구현) ④ A3(스펙 대기).
- **갱신**: [[status]](전면), [[adc]](A0~A2 상태·src 경로·4채널 표), [[adc_pinmap]](SOC/IRQ/구현 열), [[roadmap]](현재 위치), [[am263p_iomux_force_io_enable]](UART_write 주석·RS-485 결론), [[am263p_syscfg_soft_vs_hard_assign]](UART5 해소·AIN soft 잔존), [[am263p_adc_rti_trigger]](4채널 확장 경과), index 4건. **주의**: 4채널 실보드 전압 재검증 미문서화 → 보드 검증 완료로 단정 안 함(△).

## [2026-06-08] ingest | lp-am263p — ADC 인스턴스 배치 보강 + SysConfig soft/hard 물리배정 정본 (8kw J3.27/J3.28 작업·실보드 검증)

- **출처**: 8kw-ev-wpt-tx adc 브랜치 commit `b8b0ad8` — J3.28/J3.27 ADC 핀 추가 작업 + 실보드 검증. AM263P 플랫폼 공통 지식이라 lp-am263p concept으로, [[am263p_adc_rti_trigger]] 자매.
- **페이지 A (개명+보강)**: 직전 `am263p_adc_instance_placement` → **[[am263p_adc_instance_allocation]]** 개명(`git mv`). 보강분: 각 인스턴스=독립 SAR(자체 S/H·시퀀서·결과레지스터·ADCINT), 마지막 SOC EOC에서 coherent read, 8kw 현황(ADC1=Temp_Module2 SOC0+GA_Iin_SEN SOC1, 1 ISR=IRQ146 / ADC0=I_COIL_SEN·ADC4=I_LCC_SEN 별도), **사실/가설/모름 가름**(아키텍처=사실, △변환시간 예산 수치 미산정, △다중 인스턴스 동시 RTI 트리거 정밀 동시성 미실측).
- **페이지 B (신규)**: **[[am263p_syscfg_soft_vs_hard_assign]]** — SysConfig 논리 `$name`≠물리 페리페럴. 물리 배정이 soft(`$suggestSolution`)면 새 인스턴스 addInstance 시 솔버가 기존 배정까지 reshuffle.
  - **관찰 사고(2026-06-08, J3.27 추가)**: ADC4 추가 순간 솔버가 `CONFIG_ADC0`→물리 ADC2, `CONFIG_ADC4`→물리 ADC0으로 밀어냄. ADC AIN은 물리에 1:1 고정 → **엉뚱한 핀을 읽음**. 증상=ISR·변환 정상인데 인가전압 미추종(가장 헷갈리는 함정, 죽은 게 아님). "J3.27 추가 전 J3.28 동작"이 reshuffle-on-add 방증.
  - **부분수정 안 됨**: int_xbar 소스(`ADCx_INT1`)·base·AIN은 모두 물리 기준. int_xbar만 맞추는 우회는 핀 여전히 틀림.
  - **수정(✓실보드 검증)**: hard `ADC.$assign="ADCn"`(+AIN→ADCn_AINx). 물리 맞으면 base·int_xbar 자동 정렬, C코드 무수정. 검증=`ti_drivers_config.h` `CONFIG_ADCn_BASE_ADDR`==의도 `CSL_CONTROLSS_ADCn_U_BASE`+실보드.
  - **일반화**: 보드배선 고정 모든 페리페럴은 처음부터 hard `$assign`.
  - **△ 후속**: UART5도 같은 soft 재배치인지 점검 후보 — 단 TXD 패드 P15 정상 생성 기확인이라([[am263p_iomux_force_io_enable]]) RS-485 트랜시버 DE/485_EN가 유력. **2026-06-09 점검 예정**.
- **갱신**: [[am263p_adc_rti_trigger]] §3·관련페이지에 두 자매 백링크 추가. [[adc_pinmap]] 헤더 백링크 2건. index 2줄(allocation 개명행 보강 + soft/hard 신규행). 두 페이지 상호 백링크.

## [2026-06-08] ingest | oled_tv_software — BLE(ESB)_Comm_St 구현 완료 환원 + 코드 어긋난 기록 정정

- **출처**: 커밋 `6cd7e6c` (esb 브랜치), 실보드 양방향 검증 완료.
- **새 사실 — BLE_Comm_St 구현됨**: `COMM_ST_BIT_BLE`(0x10 bit6). 판정 = **presence 리셋 윈도우** — 최근 `BLE_COMM_ST_WINDOW_MS=200` 내 수신 delta ≥ `BLE_COMM_ST_MIN_COUNT=3`이면 alive. 노드별: **02_RX_ble**(PRX) `esb_rx_cnt` delta→bit6 적재→STM32 전달; **03_TX_ble**(PTX) `esb_ack_cnt` delta→자기 LED3만; **01_RX_control** bit6→`ble_comm`→`esb \| LINK UP/DOWN` 콘솔. 각 nRF가 자기 수신으로 독립 판정(02→03 verdict 못 보내 03이 ACK로 우회). 심볼 `ble_comm_st_*` ↔ `spi_comm_st_*` 대칭. throughput 아닌 presence("오긴 오나")로 합의, N=3 헐거움.
- **race-free 교훈(실보드 플래핑으로 발견)**: wire 상태비트(bit5/6)는 공유 RX 버퍼 `esb_pkt[0]`이 아니라 **송신 복사본 `spi_tx_pkt`에 `SPI_Loop` 송신 직전 stamp**. ESB RX ISR이 0x10 수신마다 `esb_pkt[0]`을 memcpy로 덮어 race→01 LINK 플래핑(49→30→0/30s). bit5는 5초 freshness로 가려졌고 즉시 읽히는 bit6만 표면화. 판정과 wire 적재 분리가 race-free 자리. → [[comm_state_monitoring]] "race-free stamp".
- **코드와 어긋난 기록 정정**: ① `ble_link` 심볼은 코드에 없음(기존 "03 ble_link 항상 0" 폐기, 실제=`ble_comm_st_bit`/`ble_comm`). ② **ESB wire 주기 = `ESB_TX_INTERVAL_MS=1ms`**(기존 "10ms"는 SPI `PACKET_INTERVAL` 혼동 오기 — [[esb_packet_format]]·[[esb_link_layer]] 정정). ③ ESB CRC는 SDK가 콜백 전 검증·폐기(`CRCSTATUS==0`)→`NRF_ESB_EVENT_RX_RECEIVED`는 CRC-valid only. ④ free-run heartbeat 설계(구 `b84b31b`, 03이 bit6 더미 토글)는 완전 폐기(03 `g_hb` 제거, `pkt_build_tx` extra_d0=0). ⑤ bit5 적재 위치도 `ESB_Loop` 인라인→`spi_tx_pkt` stamp로 정정.
- **LED**: LED3 = `ble_comm_st_bit` 미러, `LED3_PIN/ON/OFF` 매크로 수동 교체(보드별 빌드 config 폐기). 체크인 기본 DK P0.19(active-low), 회사보드 P0.06(active-high) 주석.
- **갱신**: [[comm_state_monitoring]](판정식·노드표·설계근거·race-free 절·폐기기록), [[spi_link_reliability]](bit5 stamp·ESB 1ms), [[esb_packet_format]]·[[esb_link_layer]](1ms·CRC-valid), [[tx_ble_module]](LED3 매크로), [[status]](다음=N튜닝·LED3 전환, ESB 표 3행), [[roadmap]](환원후보 완료), index 4건.
- **남은 일**: N=3 임계 실 RF 수신율 대비 튜닝(STM32 모니터 rx `LOG_EN` 게이트), 회사보드 LED3 P0.06 전환, Warning/Fault·PWM 차단 상태머신(별트랙).

## [2026-06-08] ingest | lp-am263p — AM263P ADC 인스턴스 배치 설계 규칙 정본 (8kw ADC0 추가에서 도출)

- **출처**: 사용자 제공 설계 규칙 (8kw ADC0 인스턴스 추가 작업 중 정리). 플랫폼 설계 지식이라 lp-am263p에 정본, 8kw `adc_pinmap` 백링크.
- **생성**: [[am263p_adc_instance_allocation]] (lp-am263p concept; 최초 파일명 `_placement`, 2026-06-08 후속 ingest에서 `_allocation`으로 개명·보강) — [[am263p_adc_rti_trigger]] 형제.
  - **전제 교정**: 멀티 ADC 인스턴스는 **표준·정상** 사용법(ADC0~4 존재 이유=동시 다신호 캡처). 비안정 아님. 차이는 안정성 아닌 ①동시성 ②펌웨어 복잡도.
  - **HW 사실**: 한 인스턴스 다중 SOC=**직렬**(SAR·S/H 1개 → 채널 스큐 + 변환시간 합이 트리거 주기 안에 들어와야). 다른 인스턴스=**병렬**(공통 트리거에 동시 샘플, 스큐 없음).
  - **결정 규칙**(안정성 아닌 신호 특성 기준): 상관·고속(V·I 쌍·코일/입력 전류, 제어루프) → 인스턴스 분산+공통 트리거. 무상관·저속(온도) → 한 인스턴스에 몰고 마지막 EOC 인터럽트 1개.
  - **복잡도 비용**: 인스턴스 +1 = +ISR 1·+int_xbar 라우팅 1·+ready flag 1 (8kw ADC0가 이 비용). "무상관 신호 한 인스턴스에 먼저 채우기"는 복잡도 tiebreaker(안정성 아님).
  - **유일한 실제 instability**: SOC 변환시간 합 > 트리거 주기 → 결과 밀림/덮어씀. 멀티 인스턴스 분산으로 해소.
  - **8kw 적용 메모**: PCB 라우팅이 배치 고정. 현 ADC1=Temp_Module2+GA_Iin_SEN 동거(입력 전류가 온도와 직렬) → 현 보드는 그대로 운용, 다음 보드는 입력 전류를 GA_Vin과 동시 샘플 가능하게 별도 인스턴스 검토.
- **갱신**: [[adc_pinmap]] 헤더에 배치 근거 백링크 추가. index 1건.
- **부가 정정**(직전 별건): 8kw ADC 핀맵 `GA_lin_SEN`→`GA_Iin_SEN`(입력 전류, GA_Vin의 짝) 오타 정정 — adc_pinmap·roadmaps/adc·status·index 라벨/설명 통일.

## [2026-06-08] ingest | lp-am263p — AM263P IOMUX PADCONFIG force_io_enable 정본 (UART5 사례, 8kw 미동작 조사)

- **출처**: 코드·헤더 교차검증 — `pinmux.h:93-100`(force 매크로), `pinmux.c:56-58,85-100`(KICK 매직값·plain-write), `cslr_soc_baseaddress.h:416`(IOMUX base 0x53100000), `cslr_iomux.h:395-396`(KICK offset), `pinmux.h:222-223`(EPWM15 offset), lp-am263p `evaluations/uart5/empty.c:52-88,107-113`(loopback force_io), 8kw `src/eta_bsp/eta_uart5.c:64-94,121-122`(TX 전용 force_io), 두 프로젝트 `ti_pinmux_config.c:42-51`(syscfg 생성 PADCONFIG).
- **생성**: [[am263p_iomux_force_io_enable]] (lp-am263p concept) — 플랫폼 정본. AM263P ADC·flash 정본과 동일하게 **플랫폼 지식은 lp-am263p, 8kw는 백링크** 패턴.
  - **확정**: ① PADCONFIG OE/IE override 2비트 필드(OUTPUT [7:6], INPUT [5:4]), `01`=force-enable/`11`=disable/`00`=IP default. ★OE/IE active-low 아님 — 켜려면 `|=0x40` OR-set(타 TI SoC 직관과 반대). ② SysConfig는 override를 `00`으로 남기고 `Pinmux_config()`는 plain write(`CSL_REG32_WR`, RMW 아님) → syscfg 단독으론 alt-function 패드 버퍼 절대 안 켜짐. KICK 언락 후 PADCONFIG RMW(force_io_enable) 필수. ③ 좌표: IOMUX base 0x53100000, UART5_TXD=EPWM15_A=P15=0x124(절대 0x53100124), RXD=EPWM15_B=R16=0x128.
  - **일반화**: UART5는 발견 경로일 뿐, EPWM15를 alt-func로 빌려 쓰는 모든 패드(및 다른 alt-function 패드)에 동일 적용.
  - **8kw 결론**: UART5 미동작은 펌웨어 IOMUX 원인 **아님** — 8kw TX force-output-enable이 검증된 lp-am263p 예제와 byte-identical. 다음 의심 = IOMUX 밖 THVD1400 RS-485 트랜시버(U13) DE/485_EN 핀.
  - **미검증**: P15 PADCONFIG 런타임 전체 비트 분해(bit6 OE set만 확인, JTAG로 0x53100124 직접 read해 기대값 `0x541`=syscfg `0x501`|`0x40` 확정 필요). EPWM15 패드 IP default=buffer-disabled는 SDK 예제 주석 근거이며 TRM 리셋값 미확인.
- **8kw 갱신**: [[status]] 미결에 "UART5 실보드 송신 미동작·펌웨어 원인 배제·RS-485 트랜시버 의심" 추가. index 1건.

## [2026-06-08] ingest | oled_tv_software — SPI_Comm_St 구현 완료 환원 (심볼 통일 + LED2 mirror, 실보드 검증)

- **출처**: 커밋 `e5e3efc` (refactor(comm): SPI/BLE_Comm_St 심볼·네이밍 통일 + LED2 mirror), esb 브랜치, 실보드 검증 5/5 PASS (LED2 blink, spi LINK UP/DOWN 콘솔).
- **비트 의미론**: 0x10 `Data[0]` 한 바이트가 두 성격 혼재 — bit0~4=TX 보드 물리 상태(진짜 tx_status), **bit5/6=통신 링크 heartbeat 상태(TX 보드 상태 아님, 0x10에 함께 실릴 뿐)**. 이 구분이 매크로 prefix 분리 근거.
- **심볼·네이밍**: `TX_STATUS_BIT_SPI_COMM_ST`→`COMM_ST_BIT_SPI`(BLE도 동일). `hb_*`→`spi_comm_st_*`(`Heartbeat_Loop`→`SpiCommSt_Loop`), `SPI_HB_TIMEOUT_MS`→`SPI_COMM_ST_TIMEOUT_MS`(값 5000 유지), 3종 펌웨어 통일. **모니터 라벨 문자열 `"SPI_Comm_St"`/`"BLE_Comm_St"`는 문서 표시명이라 유지 — 심볼명≠라벨**. bit5 적재 위치 정정: `build_tx_pkt()` 아니라 `02_RX_ble ESB_Loop()`의 0x10 보관 직후 인라인 clear+set.
- **spi_status 통합**: heartbeat timeout(5000ms 무변화) + CRC fail 두 FAIL 경로를 단일 `spi_status`로 (LINK UP/DOWN).
- **LED**: `tx_ble_module` LED2(P0.08)=`spi_comm_st_bit` mirror로 확정(200ms 외형 동일, 비트값 미러). LED3=`BLE_Comm_St` mirror(직전 확정).
- **갱신**: [[comm_state_monitoring]](Data[0] 이중성격 표·심볼 컨벤션 표·구현현황 5/5), [[spi_link_reliability]](heartbeat 심볼 통일·적재위치 정정·LED2 row), [[tx_to_rx_packets]](0x10 bit5/6 의미 구분·심볼명), [[tx_ble_module]](LED2 mirror), [[status]](다음 시작점=ESB 차례·SPI 완료·미결 정정), index 1건.
- **남은 일**: Warning/Fault 플래그·PWM 차단 상태 머신 미구현(범위 밖). BLE(ESB)_Comm_St CRC 도착윈도우 구현이 다음 차례.

## [2026-06-08] update | oled_tv_software — Comm_St 정리: SPI는 heartbeat 유지, ESB만 CRC 재정의

- **계기·경과**: 사용자가 Comm_St 의미를 "칩 생사" → "통신 생사(CRC)"로 재고. 1차로 SPI/ESB 둘 다 CRC 재정의했으나, 사용자가 **공식 프로토콜 문서 260513이 SPI_Comm_St를 200ms 교번 heartbeat로 명시**함을 지적 → **SPI는 heartbeat 유지로 철회**, ESB만 재정의로 정정.
- **확정(사용자 결정 2026-06-08)**:
  - **SPI_Comm_St = 200ms heartbeat 유지** (공식 문서 명시·의미 타당). 토글이 SPI를 건너오는 것 자체가 SPI 통신 생존 테스트. payload 무결성(CRC)은 STM32 로컬 `spi_status`(CRC fail+hb timeout 통합 LINK DOWN/UP)가 **보조 fault 경로**로 이미 존재 — 비트 재정의 불필요, 둘이 상호보완.
  - **BLE(ESB)_Comm_St = CRC-valid 도착 윈도우로 재정의** (`최근 T 내 CRC-valid ≥ N개`). BLE "페어링" 개념이 ESB에 부재. 판정 주체는 **수신측 `02_RX_esb`**(RF는 nRF만 앎) → 0x10 bit6 적재 → STM32 전달.
- **갱신**: [[comm_state_monitoring]] — "두 비트는 서로 다른 링크" 표·판정식, SPI_Comm_St 절 heartbeat 정의 복원, BLE_Comm_St 절 ESB CRC 재정의. [[status]] 다음 시작점·미결 정정.
- **주의**: ESB 판정 주체는 송신 03 아니라 **수신 02_RX_esb** — 구 메모/status의 `esb_rx_cnt`·`ble_link` 위치 코드 대조 재확인 필요(코드 repo 이 PC에 부재).

## [2026-06-05] ingest | lp-am263p — AM263P ADC 브링업 정본(RTI 타이머 트리거) + 8kw adc A1 검증 반영

- **출처**: 2026-06-05 8kw-ev-wpt-tx ADC 브링업 실보드 실측(단일 핀 AIN0, 1 kSPS) + TI SDK `examples/drivers/adc/adc_soc_rti`. flash-time 도구 정본([[jtag_flash_harness]])과 동일 패턴으로 **AM263P 플랫폼 지식 정본을 lp-am263p에 둠**, 8kw가 백링크.
- **생성**: [[am263p_adc_rti_trigger]] (lp-am263p concept) — 3절:
  - **§1 RTI→ADC SOC 트리거 결선 함정(핵심)**: `soc0Trigger=ADC_TRIGGER_RTI1`만으론 부족. RTI 인스턴스 SysConfig `enableIntr0`(Enable Compare Interrupt) 미설정 시 생성 코드가 `RTI_intDisable(..INT0_FLAG)`를 내보내 INT0 이벤트 export가 막힘 → ADC SOC가 tap하는 라인 게이트 닫힘 → compare 발생해도 변환 0회. 해결=`enableIntr0=true`. DMA-trigger 불필요, ISR 본체 자동 생성. 레퍼런스 `adc_soc_rti`와 유일 차이가 이 한 줄.
  - **§2 JTAG/RAM 레지스터 검증 측정 시점 함정**: `loadProgram` 후 reset 없이 read하면 `Drivers_open()` 실행 전(전부 0) 상태를 봐서 "ADC 미설정" 오진. 절차 `reset→reload→run→main loop 도달→read`. SW force(`ADCSOCFRC`)로 변환 경로 생존 먼저 확인 = "설정 문제 vs 트리거 결선 문제" 분리 기법.
  - **§3 검증된 설계 패턴**: RTI 주기 트리거 + EOC ISR(결과 read+flag) + main 루프 consuming(ISR-flag). SPS=RTI compare 주기. AIN0 1 kSPS 검증 완료.
- **8kw 갱신**: [[adc]] A1 ✓(polling→RTI 트리거 설계 전환 명기)·A0 △(단일 채널만)·A1.5 신설(UART 1초 주기화[조절 파라미터]+`src/bsp/adc.{c,h}` 다핀 리팩토링). [[status]] 다음 시작점=UART 주기화→리팩토링→남은 핀(A2), 현황표·미결 갱신. [[roadmap]] task 상태·현재 위치 갱신. index 1건.

---

## [2026-06-05] ingest | oled_tv_software — buck RF 지령 경로·UART 수신 메커니즘·newlib float 함정 + 작업 로드맵 2건

- **buck end-to-end 경로 (실보드 검증)**: 신규 [[buck_vout_ref_command_path]]. 01 UART5 `buck <v>` → 전역 `rx_cmd.tx_buck_vout_ref`(float, 0~300V clamp) → 0x51 `DATA[6,7]` `u16=volts×100`(`_shared/oled_tv_protocol.c` build_rx/apply_rx) → 03 Monitor `tx_buck_vout_ref=<raw>`. 검증 `buck 123.34`→`12334`. **01 UART 커맨드 중 RF 링크 건너 tx-nrf까지 가는 유일한 지령** — 새 tx 지령 추가 패턴(키워드 접두·`rx_cmd_t` passenger·protocol.c 매핑) 정리. 커밋 `eca4d96`(추가)/`175a8f7`(키워드 단축).
- **UART 명령 레퍼런스·수신 메커니즘**: [[uart_command_set]] 갱신 — `buck`(RF 지령)·`stop` 추가, 명령 요약표 신설. 수신·파싱 메커니즘 절: ISR 구동(`HAL_UART_Receive_IT` 1바이트→`UART5_IRQHandler`→`HAL_UART_RxCpltCallback`, 매 바이트 자기 재무장, IRQ pri 14), `cmd_buf[64]` 라인 파싱(63자 초과 폐기), **파싱·실행이 ISR 컨텍스트에서 main loop 선점**, else-if `strncmp` prefix 매칭(분기순=우선순위, `stopXYZ`도 `stop`에 걸림, `phase ` 끝공백 필수).
- **newlib-nano float 빌드 함정**: 신규 [[cubeide_newlib_nano_float]]. `01_RX_control/.cproject` `nanoprintffloat=true`(Debug만)·`nanoscanffloat=true`(이번 세션 활성화). 꺼지면 `buck 15.5` `sscanf("%f")` 소수 깨짐. GUI 경로(MCU/MPU Settings)·구성별 독립·Release 재확인 주의.
- **01 메인 루프 교정**: [[rx_control]] "메인 루프" 절 신설 — 실제 `while(1)`은 `adc_proc(); spi_proc(); Monitor_Loop();` 3개(`Core/Src/main.c:128-130`). 코드 repo CLAUDE.md의 `LED/SPI/ESB/Monitor_Loop` 4종 polling 묘사는 **nRF52(02/03) 펌웨어용** — 코드가 정본. **현재 01 `Monitor_Loop()` 주석처리 비활성**(커밋 `175a8f7`, 03 모니터로 검증하느라 임시로 끔) — [[status]] 미결에 기록.
- **CON2 핀맵**: 변경 없음 — 이미 [[rx_ble_module]]·[[schematic_ble_module_board_v01e00]]에 확정 기재(1 COMM_P5V·2 TXD_uC/P0.15·3 RXD_uC/P0.14·4 COMM_GND, 사용자 확인 2026-06-05). 확정 상태 재확인만.
- **작업 로드맵 2건 (아이디어·미착수)**: [[roadmaps/pc-gui]](G0~G3, UART 모니터링+buck 설정, G0 포트 조합 결정 선행), [[roadmaps/spi-esb-refactor]](R1~R4, 기존 코드 정리 4라운드 흡수). [[roadmap]] 환원 후보·[[status]] 예정 작업에 등재. index 5건.

---

## [2026-06-05] ingest | oled_tv_software — BLE Module Board 회로도 재독·교정 + raw 확보

- **계기**: 사용자가 `BLE_Module_Board_Ver0.1E00_260318 1.pdf` 재ingest 요청 → 이미 [[schematic_ble_module_board_v01e00]]로 ingest됨 확인. 중복 생성 대신 실제 PDF(4시트) 재독으로 미확정 해소·교정.
- **raw 확보**: PDF를 `raw/BLE_Module_Board_Ver0.1E00_260318.pdf`로 복사(483KB), source frontmatter를 raw 경로로 전환. subsystem `02_RX_ble` → `02_RX_ble, 03_TX_ble`(공용 커스텀 모듈).
- **커넥터 핀번호 확정(사용자 확인)**: CON1(SWD) 1 SWDCLK·2 SWDIO·3 nRST·4 GND·5 BLE_P3V3 / CN2(SPI 10P) 1·2 PD3V3·3 nCS·5 MISO·7 MOSI·8 SCK·9·10 DGND(4·6 NC) / CN1(전원 6P) 1~3 COMM_P5V·4~6 COMM_GND. 기존 "확인 필요" 전부 해소. [[st_link_nrf52_flash]] 미확정의 CON1 항목도 해소 표기.
- **전원 아키텍처 교정(모순 해소)**: 기존 페이지 "COMM_P5V(5V)→B1+FLT1→BLE_P3V3"는 오기. 회로도 `전원분리` 블록 실측 = **PD3V3(비절연 3.3V, CN2)→B1 페라이트(SHH-1M2012-221)+FLT1 피드스루(NFM41PC155B1H3L)→BLE_P3V3=nRF VCC**(강압 없음, EMI 필터). COMM_P5V(절연 5V, CN1)은 ISO6721 PC측+CON2 전용. One Point=R5 0Ω DGND↔BLE_GND. (이미 [[st_link_nrf52_flash]]가 "PD3V3 직결"로 맞게 적혀 있던 것과 정합 — 두 페이지 모순 제거.)
- **신규 디테일**: System Reset 회로(SW1 ITS-1107+R12 풀업/R13 직렬/C12 디바운스), 안테나(L1 3.9nH π-매칭→PCB 패턴 안테나, C8/C9 DNP), nRF 내장 DC/DC 인덕터 L2/L3(MLZ1608, 외부 LDO 아님).
- **B1/FLT1 미확정 해소**: 블록 제목 `전원분리`로 필터 확정(강압 아님).

---

## [2026-06-05] ingest | lp-am263p — AM263P JTAG flash 자동화 하네스 + 굽기 운영 규율 (정본)

- **출처**: 2026-06-05 8kw-ev-wpt-tx 실보드 JTAG flash 세션 실측. 도구(jtag_flasher·flash_node.js)는 lp-am263p(cc3351) 원산·8kw 복제 → **flash-time 도구 지식 정본을 lp-am263p에 둠**.
- **생성**: [[jtag_flash_harness]] (lp-am263p concept) — 4대 규율 전부 측정 확정:
  - ① **하네스**: run.bat Node.js `runAsynch`+`run(false)`+`gCmd.status` 폴링 = 6/6 OK. **DSS/Rhino `GEL_RunF`는 깨짐** — GEL_RunF resume가 R5를 JTAG halt 없이 free-run, 그 상태 DSS `readData`로 TCM(`gCmd.status@0x70038010`) 읽으면 `Error 0x400000` 거부 → status 폴링 붕괴.
  - ② **클린 호스트**: IDE 상주 cloudagent+DSLite 경합(요지만, deep-dive는 [[jtag_flash_clean_host]] 위임).
  - ③ **파워 사이클 필수**: 연속 loadProgram/soft reset/중단런으로 R5/OSPI wedged → run 후 status IDLE(0x0)→never BUSY/300s timeout. 전원 차단→복원만 해소(JTAG 재연결 불가). 측정: OP1 ~61s IDLE 탈출, 3/3.
  - ④ **검증 ground truth = standalone 부팅 banner**: 하네스 자기보고/MCP readback보다 정확. 프로파일: NOR SPI FLASH·16.667MHz·30KB·SBL ~28967µs·banner `eta-tx: 8kw-ev-wpt v1.0e00`.
- **보조 사실**: flashwriter(`jtag_flasher.out`=`sbl_jtag_uniflash`+`AutoCmd_t`) gCmd base `0x70038000`/status `0x70038010`/magic `0xDEAD1234`/파일버퍼 `0x70040020`. flash map SBL@`0x0`·app mcelf@`0x81000`. PHY 경고(`PhyTune:1520 PHY enabling failed`) 무해(부팅 성공이 증거). SW1 standalone=`1,1,1,1`/DevBoot=`0,1,0,0`. 하네스 위치 `8kw-ev-wpt-tx/tools/jtag_flash/flash_node_8kw.js`.
- **DevBoot 오기**: 이미 [[CLAUDE]]에서 정정 완료(`1,1,0,0`→`0,1,0,0`, commit 0b59571) — wiki 내 잔존 stale 없음(정정 주석/raw만). 신규 페이지는 정정값 인용.
- **빈자리**: OSPI 독립 readback 미검증(standalone 부팅으로 대체). 갱신: [[flash_open_facts]]·[[jtag_flash_clean_host]] cross-ref, index 1건.

---

## [2026-06-05] ingest | 8kw-ev-wpt-tx — JTAG flash 굽기는 CCS IDE 내린 클린 호스트에서

- **운영 함정 확정 (격리 입증)**: AM263P OSPI를 JTAG로 굽는 host-driven 스크립팅(`run.bat`/Node.js `flash_node.js`, 또는 DSS Rhino)은 CCS IDE(Theia)의 상주 cloudagent+DSLite 디버그 백엔드와 **같은 디버그 백엔드를 두고 경합**. IDE 켜둔 채 flash 돌리면 `ds.configure()`/`openSession`/`resume` 중 런마다 다른 지점에서 죽음 (30s ScriptingTimeoutError / DebugServer.1 timeout / rd32 Error 0x400000 — **비일관 → 펌웨어·보드 결함으로 오인 위험**).
- **증거**: flashwriter `.out` 바이트 동일(펌웨어 무죄)인데 **IDE 켜둠=ERASE_ALL 실패 / IDE 완전 종료=6/6 OK 완주**. 변수는 IDE 상주 여부 하나뿐.
- **확인법 함정**: `getDebugSessions=[]`라도 cloudagent가 띄운 DSLite는 상주 가능 → 작업관리자에서 `node`/`DSLite` **프로세스 레벨**로 확인 후 종료.
- **양립 불가**: MCP `loadProgram`(IDE 경유 RAM 로드)은 IDE 켜짐 필요 / 독립 flash 스크립팅은 IDE 꺼짐 필요.
- **생성**: [[jtag_flash_clean_host]] (8kw concept). index 1건. lp-am263p [[flash_open_facts]]에 cross-ref 추가 (app Flash_open 블로커 ≠ flash-time 호스트 함정, 층위 구분).

---

## [2026-06-05] ingest | oled_tv_software — 플래싱 듀얼 프로브 셋업 (드라이버 스왑 종료)

- **사실 확정 (CLI 실측)**: MCU별 전용 프로브 + 네이티브 도구로 분담. ① `01_RX_control`(STM32F103) → **ST-Link V2 네이티브**(STM32_Programmer_CLI v2.22, FW V2J47S7, Device ID 0x414, connect+read만 실측 — write 미측정). ② `03_TX_ble`(nRF52832 회사보드) → **J-OB v2 = J-Link OB-nRF5340-NordicSemi** S/N 1050329071(정품), program+verify 통과(Bank0@0x0 53248B, exit 0). ③ `02_RX_ble` → DK 온보드 J-Link. 드라이버 분리 → 동시 연결·충돌 없음.
- **함정**: J-Link급 프로브 둘(J-OB v2 + SAM-ICE S/N 24012600) 공존 → `-SelectEmuBySN 1050329071` 고정 필수. ST-Link은 S/N이 `@`로 보고(cosmetic).
- **갱신**: [[st_link_nrf52_flash]] 전면 재작성(정본 — 듀얼 프로브 절차·실측·함정, **pyOCD+Zadig 폴백 강등**, ST-Link WinUSB→네이티브 원복 절차). [[instruments]] "프로그래밍/디버그 프로브" 절 신설(프로브 3종 정체·S/N·드라이버). [[rx_ble_module]] CON1 플래싱 비고 갱신. index 2건.
- **교정**: 회사보드 CON2 UART = **TX P0.15 / RX P0.14**(`custom_board.h:16-17`), NRF_LOG는 RTT(SWD) 전용·UART 미출력. (schematic 소스는 2026-06-04에 이미 정정됨 — 잔존 stale은 st_link 페이지 "미확정" 항목뿐이었고 재작성으로 해소.)
- **빈자리(미검증)**: SES 번들 JLinkARM DLL의 SN 선택 동작, ST-Link 실플래시(write), 플래시 펌웨어 런타임 거동(ESB/SPI/LED), SAM-ICE 연결 대상.

---

## [2026-06-05] lint | lp-am263p — SW1 부트모드 표 DevBoot 값 정정

- **오류**: `teams/g/lp-am263p/CLAUDE.md` SW1 표가 DevBoot를 `1,1,0,0`으로 기재 → 실제로는 OSPI (8S) Octal Read 값의 오기.
- **정정**: DevBoot = `0,1,0,0`(SW1.3만 ON). 근거 LP-AM263P UG SPRUJ85B Table 2-5 ([[raw/lp_am263p_ug/ug_lp-am263p.md]] :469), DevBoot 정의 Table 2-6 :494.
- **부가 수정**: 기존 헤더 `SW1 (1,2,3,4)` 라벨이 실제 기입값(UG의 SW1.4-우선 순서)과 불일치 → 헤더를 UG 순서 **SW1.4/3/2/1**로 명시. 전체 6개 모드 값을 Table 2-5와 교차확인해 표 정합성 확보. ON=논리0(:453) 주석 추가.

---

## [2026-06-05] status | oled_tv_software — 회사 커스텀보드 플래싱·LED 점멸 확인 반영

- **사실 확정**: 회사 커스텀보드(BLE_Module_Board_Ver0.1E00, nRF52832) 입고 + `03_TX_ble` ST-LINK V2 + pyOCD 플래싱 성공 + LED 점멸 육안 확인(LED1 상시점등·LED2/LED3 200ms 토글, active-high). 절차·셋업 함정은 기존 [[st_link_nrf52_flash]]에 정리됨(2026-06-04).
- **status.md 갱신**: stale했던 "다음 시작점"(완료된 ST-LINK 플래싱 지목)을 **LED2/LED3 ↔ 실제 comm-status 비트 연계**로 교체. 하드웨어 입수 표에 플래싱 열·LED 확인 추가. frontmatter date → 2026-06-05.
- **예정**: 플래싱 이슈·해결 추가 공유 시 [[st_link_nrf52_flash]] 트러블슈팅에 ingest.

---

## [2026-06-05] ingest | AM263P TRM/UG wiki 통합 + RAG MCP 폐기

- **결정**: AM263P 자료를 위한 별도 RAG MCP 서버(`C:\firmware-rag\`, ChromaDB 벡터검색 + 800단어 청크 + all-MiniLM-L6-v2)를 폐기하고 wiki 단독으로 전환. 근거: ① wiki 철학 = "원본 텍스트가 아닌 이해된 지식" ② 800단어 청킹이 레지스터 표를 절단(TRM 질의의 핵심 손상) ③ "wiki 단독 ≠ LLM이 1725쪽 정독" — 기계추출(토큰 0) + Grep 발견 + demand 환원 구조.
- **기계추출**: `pymupdf4llm` 1.27.2.3로 TRM 1725쪽을 `get_toc()` 기반 26개 챕터 마크다운(텍스트+표, 이미지 제외)으로 → `raw/am263p_trm/chNN_*.md`. ch7·ch13만 level-2 세분. UG 60쪽은 이미지 포함 전체 → `raw/lp_am263p_ug/`(md+img 42장).
- **source 페이지**: [[am263p_trm]](TOC 맵 + "발견은 Grep" 가이드 + ingested/candidate 섹션 인덱스), [[lp_am263p_ug]](핀맵·부트모드·핀먹스·OSPI 배선 + §5.3 보드 함정 — DQS/LBCLK swap·XDS110 bricking).
- **demand-ingest 예시**: [[am263p_mcspi_controller]] — S6 `SPI not responsive` 직결 MCSPI(13.1.3) 환원.
- **폐기 처리**: `~/.claude.json`의 `ti-am263p` mcpServers 등록 제거(재시작 시 도구 사라짐, 다른 CCS 서버 보존). 22MB TRM PDF는 `.gitignore`(디스크 only). `C:\firmware-rag\` rm_db/스크립트 삭제는 사용자 확인 대기.

---

## [2026-06-05] status | 8kw-ev-wpt-tx — CCS 프로젝트 스캐폴드 완료 반영

- A0 전제 완료: hello_world 기반 CCS 프로젝트 생성·Release 빌드 통과·커밋됨 → 구현 현황 ✓ 갱신.
- 다음 시작점 업데이트: A0 착수 전 SysConfig MCP 버전 정합 확인 절차 추가.
- `직전 완료` 섹션 신설 — CCS workspace 참조 import 작업환경 메모 포함.

---

## [2026-06-04] ingest | 8kw-ev-wpt-tx 프로젝트 신설 + adc 작업 호 개설

- eta 보드 J3 커넥터 6채널 ADC 핀맵(사용자 제공) → [[adc_pinmap]] 엔티티 생성.
- `adc` 작업 로드맵(A0~A4) 신설: SysConfig 설정 → 단채널 검증 → 전채널 읽기 → 신호별 스케일링 → 실보드 교차검증.
- A3(스케일링) 블로커: Temp 모듈 특성·전류 센서 감도·분압비 미입수 — 추가 정보 대기.
- lp-am263p에 잘못 붙었던 eta-adc 항목 모두 제거 후 이 프로젝트로 이관.
- 신규 프로젝트 `teams/g/8kw-ev-wpt-tx` 생성 — 8kW EV WPT 송신 보드 Ver1.0E00, LP-AM263P 기반.

---

## [2026-06-04] ingest | oled_tv_software 03_TX_ble LED 인디케이터 + 보드 분기

- 03_TX_ble LED 3개 구현·실보드 검증: LED1(P0.09) System Ready 상시 점등, LED2(P0.08) SPI Comm Status·LED3(P0.06) BLE(ESB) Comm Status 200ms 토글. 극성 **active-high(1=ON)** 실측 확정.
- LED 핀맵 정정 과정: 초기 잘못된 핀(10/9/8) → 실측 혼선 → 정정(9/8/6, = `_shared/oled_tv_protocol.h` 원래 값). 극성도 active-low 오판정 → 정정해 active-high 확정.
- DK(PCA10040) ↔ 회사 보드 핀맵 분기: `_shared/custom_board.h` 신설(`LEDS_NUMBER 0`, UART RX=14/TX=15) + emProject `BOARD_CUSTOM`. LED 코드는 `#if defined(BOARD_CUSTOM)` 가드 — DK에선 P0.06/08이 UART라 충돌 회피.
- 갱신:
  - [[schematic_ble_module_board_v01e00]] — LED 인디케이터 GPIO 핀(P0.09/08/06)·극성, CON2 UART 핀(P0.15/14) 채움
  - [[gpio_verification_pinmap]] — 03_TX_ble LED 검증 행 3개 추가, P0.17 중복 주석 "PCA10040" → "커스텀 보드" 정정
  - [[tx_ble_module]] — LED 인디케이터·보드 분기 섹션 신설 + 현황표 2행 추가

---

## [2026-06-04] ingest | oled_tv_software ST-LINK V2 + pyOCD nRF52832 플래싱 절차 확립

- 계기: BLE_Module_Board_Ver0.1E00(nRF52832)에 `03_TX_ble` 플래싱 성공. SES 내장 다운로더·nrfjprog가 J-Link 전용이라 ST-LINK로 사용 불가 → pyOCD 우회 경로 확립.
- 핵심 함정 3개 (Windows Python 3.14 환경):
  1. `libusb-package` 바이너리 wheel 없음 → cp311 wheel에서 `libusb-1.0.dll` 수동 추출·복사
  2. ST-LINK WinUSB 바인딩(Zadig) → STM32CubeIDE 플래싱 불가(부작용), 장치 관리자로 복구
  3. `target_nRF52.py` CTRL-AP 패치 — `is_locked()`에서 `ProbeError` try/except → `return False` (ST-LINK V2가 AP#1 접근 불가)
- 추가 환원: ST-LINK 드라이버 토글 절차 (WinUSB↔ST 정품, 양방향·모드 확인·동글 2개 팁)
- 생성:
  - concepts: [[st_link_nrf52_flash]] (플래싱 how-to — 셋업·배선·절차·트러블슈팅·드라이버 토글·미확정)
- 갱신:
  - [[status]] — 다음 시작점 참고 줄에 [[st_link_nrf52_flash]] 링크 추가
  - [[rx_ble_module]] — CON1 비고에 역링크 추가
  - [[index]] — Concepts 섹션에 st_link_nrf52_flash 등록
- 미확정 잔류: CON1 물리 핀번호↔네트 매핑 (실크 Pin1 확인 필요), CON2 UART nRF GPIO 핀 라우팅

---

## [2026-06-01] ingest | oled_tv_software SPI 10ms 폴링 진단 (미달 반증·✓ 확정)

- 소스: 진단 세션 직접 보고 + 오실로스코프 캡처 `P3NOFO01.PNG` (CS Δt=10ms, 1/Δt=100Hz, Vpp=3.79V)
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble
- 결론: "SPI 10ms 미동작"은 동작 결함이 아닌 **관측 도구 한계** (단일 필드 덮어쓰기). 10ms 폴링은 처음부터 정상.
- 생성:
  - sources: [[spi_10ms_diagnosis_report_260601]] (진단 경과·3가지 가설 반증·실보드 검증 결과)
  - assets: `spi_cs_10ms_260601.png` (오실로 캡처 — 기존 heartbeat `P3NOFO01.PNG`와 별도)
- 갱신:
  - [[spi_link_reliability]] — "미달 — SPI 10ms 폴링 ✗" → "SPI 10ms 폴링 주기 ✓", 오류율 모니터 카운터명/출력형식 정정(`spi_crc_fail_cnt`·누적+delta), `spi_tx_busy` 주석 정정(근본원인 미확인), 관련 백링크 추가
  - [[status]] — date 갱신(05-29→06-01), 다음 시작점(nRF52832 SPIS SCK datasheet ingest), SPI 10ms ✗→✓, 오류율 모니터 메모 갱신, "SPI 10ms 미동작 원인 규명" 미결 제거
  - [[index]] — spi_link_reliability 설명 갱신, 신규 source 등록
- 핵심 합의: NVIC enable은 `MX_DMA_Init()`에 정상 존재(`app_dma.c:15-19`). `PACKET_INTERVAL=10`도 이미 설정됨. 초당 100tx, CrcFail=0 확인. "미동작" 의심은 `rx_status.spi_status` 단일 필드 덮어쓰기 관측 한계.

---

## [2026-06-01] roadmap | lp-am263p 포팅 로드맵 project/task 분리 + spine 정리

- 계기: 앞으로 프로젝트·작업 로드맵을 wiki에서 작성. 외부 코드-repo `tasks/porting/roadmap.md`는 이미 2026-05-29 wiki `roadmap.md`로 ingest됨(외부보다 wiki가 최신: R27/R28 vs R24/R26) → 외부 파일 legacy화, 기존 wiki roadmap을 비판적으로 개정.
- 비판 검토에서 잡은 수정:
  - A. staleness — §6 "24라운드째"가 R27+와 어긋남(외부 R24 잔존) → R27로 정정.
  - B. "2~4주" false precision — 문서 스스로 "추정 불가"라면서 단일 숫자 제시 → 삭제, S3 게이트 기반 통일.
  - C. S5~S8 난이도 grading — 전부 미도달인데 등급 부여 → "S3 통과 후 재추정"으로 축약.
  - D. altitude 과적재 — §1 칩차이·§3 HW표가 spine 아님 + CLAUDE.md와 중복 → 백링크 위임.
  - E. §7 환원후보 80% 해소 방치 → 미해소 1건만 남기고 나머지는 "facts/handoff 반영 완료" 한 줄.
  - F. §2 "가능성 높음" 약과장 → "불가 근거 없음·미증명"으로 완화·압축.
- 구조 결정(사용자): project/task 2단위로 분리.
  - 신규 `roadmaps/porting.md` — 작업 호. S0~S8 spine·완료 기준 표·현재 위치(→status)·남은 일정·환원후보. 엄격 spine(§1 칩차이→[[is25lx256_vs_spansion_quirks]], 핸드오프→[[sbl_app_flash_handoff]], HW→[[CLAUDE]] 위임).
  - `roadmap.md` 개정 — 얇은 프로젝트 호. 목표·작업 호 인덱스(1행)·현재 위치만. S0~S8 재서술 금지(divergence 방지) → [[porting]] 위임.
- 갱신: [[lp-am263p]] `CLAUDE.md` 3-레이어 표(전략을 프로젝트/작업 2단으로), [[index]].
- 손대지 않음: `status.md`(라운드 갱신 아님, 다음 시작점 R28 유지), [[flash_open_facts]]·[[flash_open_diagnostic_log]](사실/history 단일 소스).

---

## [2026-06-01] schema | 파이프라인 도메인 자산 — 계측 인벤토리 + GPIO 검증 핀맵 + 로드맵 컨벤션

- 계기: `~eta/firmware-dev-pipeline` 두 단계(explorer/planner)가 wiki를 읽어 쓰도록 갱신됨. 그 계약을 wiki schema에 맞게 세 자산으로 빚음.
- 합의: 시작 컨텍스트 `teams/c/oled_tv_software`(핀맵 seed 풍부), 로드맵은 별도 `roadmap.md`(status 확장 아님, lp-am263p 선례), 인벤토리는 root `pages/reference/` 신설, 작업 로드맵은 `roadmaps/<task>.md`.
- 생성:
  - reference: [[instruments]] (회사 공통, Keysight InfiniiVision MSOX3104T — 무엇을·어떻게 측정 + 사용 결. 추가 장비 스텁)
  - oled concepts: [[gpio_verification_pinmap]] (기능→프로브 핀→기대값. 기존 wiki 사실만 seed, 미확인 핀은 "확인 필요"로 호명 — 추론 금지)
  - oled `roadmap.md` (M0~M6 마일스톤 호, 현재 M3 SPI 10ms 막힘, PRD 1~2ms 지연 게이트). lp-am263p 선례 결 계승
  - oled `roadmaps/README.md` (작업 로드맵 폴더 컨벤션 — 파일은 요청 시)
- 갱신:
  - root `CLAUDE.md` — 레이아웃에 reference/·roadmap.md·status.md·roadmaps/ 추가, "로드맵 컨벤션" 절 신설, "파이프라인 — roadmap 읽기/갱신 절차" 절 신설(explorer/planner 읽기 전용·wiki 작성)
  - [[lp-am263p]] `CLAUDE.md` — 3-레이어 표가 root 로드맵 컨벤션의 프로젝트별 구현임을 명시 (중복 정의 회피)
  - oled `CLAUDE.md` — 전략/검증 자산 절 추가 ([[roadmap]]↔[[status]], [[gpio_verification_pinmap]], [[instruments]])
  - [[index]]
- 핵심 결정: 읽기=파이프라인, 작성·갱신=wiki. planner는 핀번호를 추론하지 않고 wiki에 없으면 "확인 필요"로 사용자 호명. 핀맵은 P0.17 의미 충돌(TX 시작 03 vs heartbeat 02)과 RX_control 추가 GPIO 핀번호를 미확정으로 남김 — 사용자 호명 대기.

---

## [2026-05-29] ingest | lp-am263p report.md R19~R27 — 사실 원장/라운드 로그 분리 + CLAUDE.md schema 신설

- 소스: `~/eta/projects/g/lp-am263p/bp-3351/tasks/porting/report.md` (R19~R27 + R28 계획)
- 대상 프로젝트: `teams/g/lp-am263p`
- 핵심 합의: 초장기 디버그 작업의 맥락유실 방지를 위해 "작업 중 밝혀진 사실"을 **사실 원장(제자리 수정) + 라운드 로그(append-only) 2분리**. 3-레이어 = 로드맵(전략)/status(전술)/facts·log(누적).
- 생성:
  - concepts: [[flash_open_facts]] (확정 사실 + **폐기 가설(재시도 금지)** + 최유력 가설), [[flash_open_diagnostic_log]] (R7~R27 + R28 계획, append-only)
  - [[lp-am263p]] 도메인 `CLAUDE.md` 신설 (부재했음) — 3-레이어 분류·SW1 부트모드·boot flow·"자주 어긋나는 자리"
- 갱신:
  - `roadmap.md` — Round 24+→27+, **R26 반증된 `DQS_ENABLE=0` "검증 예정" 줄 제거**(stale), facts/log 위임 백링크, §7 환원후보 1·2·4·5 해소 표시
  - `status.md` — 빈 템플릿 채움: 다음 시작점 R28(jtag_flasher 공식 이식), S0~S8 현황표, 미결 4건
  - [[sbl_app_flash_handoff]] — 후보1에 R25~27 실측, 신규 §flashFixUpOspiBoot 부재(app vs flasher 비대칭), §SW1 4S 핸드오프 질문, 후보3 DQS는 R26 검증(DQS 필수·DQS=0 반증)
  - [[is25lx256_vs_spansion_quirks]] — set888mode=0x81 정정(0x71 혼동 종결), AM243 Quad/AM263P Octal 라인 차이
  - [[index]]
- 핵심 결정: R25(skipHwInit=FALSE)·R26(DQS=0) 두 진단 가설 폐기 기록 → 다음 세션이 facts.md만 읽고 재시도 방지. 최유력 가설 = SBL 잔여 8D + skipHwInit=TRUE 캡처 미스, R28에서 flasher 성공 공식 이식으로 검증.

---

## [2026-05-29] ingest | SPI heartbeat 작업 보고서 (260529)

- 소스: `tasks/spi-heartbeat/report.md` + 오실로 스크린샷 `P3NOFO01.PNG`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
- 생성:
  - sources: [[spi_heartbeat_report_260529]]
  - concepts: [[spi_link_reliability]] (heartbeat 구현·오류율 모니터·spi_tx_busy 타임아웃 복구·10ms/9MHz 현황)
- 갱신:
  - [[comm_state_monitoring]] — 200ms 교번 사양이 코드(Heartbeat_Loop 200ms 독립 타이머)로 실현됨 확정 + 백링크
  - [[spi_packet_format]] — 전송 파라미터 "10ms/9.0Mbps"를 사양으로 명시, 실측 미달(폴링 1000ms, 9MHz revert) 주석
  - [[rx_ble_module]] — Heartbeat_Loop·P0.17 디버그 핀·펌웨어 현황 3행 추가
  - [[index]], [[status]]
- 핵심 합의:
  - 모순은 wiki↔wiki가 아니라 과거 코드(매 SPI 사이클)↔사양(200ms 매뉴얼). 오늘 코드가 사양 충족.
  - heartbeat만 실보드 검증(✓). 오류율 모니터·spi_tx_busy 복구는 △. SPI 10ms 폴링·9MHz는 ✗.
  - 10ms 미달 유력 원인: STM32 `HAL_SPI_MspInit` DMA IRQ(NVIC) 부재 → 콜백 미발생.
  - "10ms" 용어 구분: 앱 SPI 폴링 주기(PACKET_INTERVAL) ≠ ESB RF wire 주기 ([[spi_debug_log_report_260529]] 미결과 동일).
  - `_ble` 파일명은 잔재이며 ESB 라인의 정식 코드 (사용자 확인).

---

## [2026-05-29] ingest | lp-am263p 포팅 로드맵 — 전략 spine

- 소스: `~/eta/projects/g/lp-am263p/bp-3351/tasks/porting/roadmap.md` (planner roadmap)
- 대상 프로젝트: `teams/g/lp-am263p`
- 생성: `teams/g/lp-am263p/roadmap.md` — 프로젝트 루트 living doc
  - 백링크 spine 방식: 단계 구조(S0~S8)·현재 위치(S3 막힘)·남은 일정만 직접 보유
  - 깊은 디테일은 기존 concept로 위임 — [[is25lx256_vs_spansion_quirks]], [[sbl_app_flash_handoff]], [[flash_open_sequence]], [[xspi_dummy_cycles]]
  - 기능별 현황은 [[status]]와 역할 분담 (로드맵=전략, status=전술)
- 갱신: `index.md` — lp-am263p 섹션에 "Living docs"(roadmap/status) 추가
- 미결: lp-am263p 프로젝트에 도메인 `CLAUDE.md` 부재 (다른 프로젝트는 모두 보유) — 별도 생성 필요

---

## [2026-05-29] ingest | SPI 디버그 로그 검증 결과 (시나리오 A/B)

- 소스: `tasks/spi-debug-log/report.md`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
- 생성:
  - sources: [[spi_debug_log_report_260529]]
  - concepts: [[esb_ptx_ack_assembly]] (PTX ACK payload 재조립 + ISR printf 금지 패턴)
- 갱신:
  - [[rx_to_tx_packets]] — 코드 실측 DATA 레이아웃 추가, 프로토콜 매뉴얼과의 불일치 정리 (0x50 bit 순서, 0x51 Zin·TxVoutRef 미구현, 0x52 T2 스케일 0.1°C 확인)
  - [[tx_ble_module]] — Monitor_Loop 출력 포맷 + [[esb_ptx_ack_assembly]] 링크 추가
- 핵심 합의:
  - 0x51 코드에 Zin·TxVoutRef 없음 — 프로토콜 매뉴얼 대비 미구현 필드
  - 0x50 bit2=BuckSt / bit3=Warning / bit4=Fault — 매뉴얼과 순서 다름
  - 0x52 T2 스케일은 코드 기준 0.1°C (매뉴얼 "0.01°C" 오기 해소)
  - PTX에서 g_last_ack_by_hdr[3] 패턴 필수 — 1초 윈도우 내 3헤더 보존

## [2026-05-27] ingest | Rx OLED Regulator Control Board 회로도 (OrCAD Design XML)

- 소스: `rx_oled_regulator_control_board_260327.xml` (OrCAD Design XML, 68,941줄) + `Rx_OLED_Regulator_Control_Board_260327.pdf`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control
- 생성: `sources/schematic_rx_regulator_control_board.md`
- 갱신: `entities/rx_control.md` (CAN·DAC·추가 GPIO 신호 추가), `concepts/adc_channel_map.md` (TEMP1/TEMP2 swap 회로도 확인으로 해소)
- 확인 사항: MCU는 STM32F103VCT6/LQFP64 (OrCAD 라이브러리명 오기), 39개 _uC 신호·24개 _CN 신호 전수 추출, TEMP1_ADC_uC=PC4 좌표 매칭 확인

## [2026-05-27] ingest | RX Control UART5 Command Reference (이미지 PDF)

- 소스: `C:\Users\echog\eta\projects\c\oled_tv_software\docs\매뉴얼 (Uart Commands)_테스트용.pdf` (6p, 이미지형)
- 대상 프로젝트: `teams/c/oled_tv_software`
- 도구: Poppler pdftoppm → PNG 변환 → Claude 시각 읽기 (첫 이미지형 PDF ingest)
- 신규 생성:
  - sources: [[uart_cmd_reference_테스트용]]
- 갱신:
  - [[uart_command_set]] — phase·start 추가, dt 구문 2인자로 수정, UART5 핀(PC12/PD2) 추가
  - [[dead_time]] — dt_ratio 개념 추가, 구버전 3인자 구문 대비 표
  - [[rx_control]] — UART5 핀 테이블 추가 (MCU RCT6 유지, PDF VCT6 오기 확인)
- 핵심 합의:
  - MCU는 STM32F103**RCT6** (64핀). PDF에 VCT6로 기재되어 있으나 문서 오기 — 사용자 확인.
  - `dt` UART 명령 구문 변경: `dt <ch> <ns> <pct>` → `dt <ch> <ns>` (duty 인자 분리됨)
  - `phase`, `start` 명령 신규 확인. start = 4채널 동시 pwm start + current_phase_deg 적용.
  - dt_ratio = 데드타임/주기. freq 명령 시 3~5% 클램프 자동 적용.

---

## [2026-05-26] ingest | CC3350/CC3351 데이터시트 (SWRS284C)

- 소스: `C:\Users\echog\eta\cc3351-datasheet.pdf` (34p, Rev.C, October 2025) — wiki 밖 보관
- 대상 프로젝트: `teams/g/bp-cc3351`
- 도구: PyMuPDF(fitz) — 전체 텍스트 추출 → 챕터별 마크다운 분할 수작업
- 신규 생성:
  - raw: `raw/cc3351_datasheet/ch01_overview.md` — Features, Applications, Description, System Diagram
  - raw: `raw/cc3351_datasheet/ch02_pin_config.md` — 40핀 다이어그램, Pin Attributes 전체 표, SPI 모드 핀맵
  - raw: `raw/cc3351_datasheet/ch03_specifications.md` — AMR/ESD/동작조건/전기특성/RF성능/전류소모/SDIO·SPI·UART 타이밍
  - raw: `raw/cc3351_datasheet/ch04_description_schematic.md` — WLAN/BLE 상세 설명, Reference Schematic 주요 연결
  - raw: `raw/cc3351_datasheet/ch05_support.md` — Tools & Software, 문서 목록, Revision History
  - raw: `raw/cc3351_datasheet/ch06_packaging.md` — Orderable Information, T&R 치수, Package Outline
  - sources: [[cc3351_datasheet]] — 소스 인덱스 + 핵심 요약 + raw 챕터 링크
- 파생 페이지 미생성 (lazy): `cc3351_ic`, `cc3351_pinmap`, `cc3351_power_rails`, `cc3351_host_interface` — lp-am263p 포팅 작업이 trigger할 때 생성
- 핵심 합의:
  - CC3350(Wi-Fi 6 only) vs CC3351(Wi-Fi 6 + BLE 5.4). Pin-to-pin 호환.
  - Host I/F: SDIO 4-bit (≤52MHz) or SPI (≤26MHz) for Wi-Fi, UART (≤4364kbps) for BLE HCI.
  - SPI 핀: CS=SDIO_D3(21), SCLK=SDIO_CLK(19), PICO=SDIO_CMD(18), POCI=SDIO_D0(24), IRQ=HOST_IRQ_WL(29).
  - 전원: VMAIN/VDDA/VIO=1.8V, VPA=3.3V. 전원 시퀀싱: 모든 공급 안정 후 nRESET low ≥10µs → 해제.
  - 클럭: 40MHz XTAL 필수(외부), 32.768kHz 슬로우 클럭 내부 생성 가능.

---

## [2026-05-26] ingest | STM32 mini-pro v10 회로도 — SPI 수동 추출

- 소스: `projects/c/oled_tv_software/docs/Schematic/회로도 (STM32F103RCT6).pdf` — 이미지 기반 PDF, 텍스트 레이어 없음. SPI 연결 부분만 수동 추출.
- 추출 내용: STM32 SPI2 핀맵 (PB12=CS, PB13=SCL, PB14=SDO, PB15=SDI — 슬레이브 관점 표기).
  - SDO(PB14) = MISO (마스터 관점), SDI(PB15) = MOSI (마스터 관점). 기존 코드 분석과 일치.
- 신규 생성:
  - sources: [[schematic_stm32_mini_pro_v10]] — 회로도 레이블·마스터 명칭 대응표 + STM32↔nRF52832 PCA10040 배선표
- 갱신:
  - [[rx_control]] SPI 절 — "transparent bridge" 오기 제거, 새 페이지 링크로 교체
- 미기록: PCA10040 커넥터 헤더 핀 번호 (GPIO→헤더 위치 매핑). 필요 시 PCA10040 Hardware Spec 참조 후 추가.

---

## [2026-05-26] ingest+restructure | PRD v1.0 ingest + SPI/ESB 프레임 분리 재구조화

- 트리거: PRD(`projects/c/oled_tv_software/docs/prd.md`) 최초 ingest. PRD에서 STM32-nRF SPI(56B/45B, HDR 0xC0)와 ESB wire(11B, HDR round-robin)가 서로 다른 포맷임이 명시됨.
- **핵심 정정**: 기존 wiki의 "무선모듈 transparent bridge, SPI 11B = ESB wire" 주장 취소. nRF가 두 포맷을 능동 변환함을 확정.
- 재구조화:
  - `spi_packet_format` 재작성 → STM32-nRF 내부 SPI 프레임 전용 (56B/45B, HDR 0xC0, 20ms)
  - 신규 `esb_packet_format` — ESB wire 포맷 전용 (11B, HDR 0x10-0x52, 10ms, ACK with payload). 기존 spi_packet_format의 ESB 내용 이전.
  - `tx_to_rx_packets`, `rx_to_tx_packets` backlink: `[[spi_packet_format]]` → `[[esb_packet_format]]`
  - `spi_protocol_manual_260513` 소스 페이지: "SPI 매뉴얼"이 아닌 "ESB wire 사양 정의 문서"로 정정. "transparent bridge" 설명 제거.
  - `rx_ble_module` — 통신 페어 절 분리(SPI 내부/ESB wire), 펌웨어 현황 표 추가.
- 신규 생성:
  - raw: `prd_v1.0.md`
  - sources: [[prd]]
  - entities: [[tx_ble_module]] — 03_TX_ble nRF52832 PTX, TX보드 SPI 미구현
  - concepts: [[esb_link_layer]] — ESB 링크 파라미터(10ms, ACK with payload, NRF_ESB_MAX_PAYLOAD_LENGTH=64), 미결 파라미터 목록
- PRD의 미해결 의문점 (기존 wiki 관련):
  1. PWM 주파수 불일치 — [[pwm_system]] 기록 있음, PRD에서 재확인
  2. ADC 물리량 변환 미구현 — [[adc_channel_map]] 기록 있음
  3-5. CAN1/DAC 용도, README 역할 오표기 — 미문서화, 후속 확인 필요
  6. SPI 하드웨어 테스트 미실시
- PRD 업데이트 시: 새 버전 `raw/prd_vX.Y.md` 추가 + `sources/prd.md` frontmatter 갱신.

---

## [2026-05-26] ingest | bp-cc3351 프로젝트 신설 + EVM User Guide ingest

- 배경: lp-am263p 포팅 원본 source 보드(BP-CC3351)를 별도 프로젝트로 분리 결정.
- 합의사항 반영:
  - `wiki/CLAUDE.md` — "크로스 프로젝트 참조 규칙 (first-ingest-wins)" 단락 추가
  - `teams/g/bp-cc3351/CLAUDE.md` — reference-only 성격·lazy ingest 원칙·cross-ref 대상 명시
- 신설 디렉토리:
  - `teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/` — EVM UG 챕터별 마크다운 6개 파일
  - `teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/` — PNG 26장 (파일명에 원본 페이지 번호 인코딩)
  - `teams/g/bp-cc3351/pages/{entities,concepts,sources}/` — scaffold
- 생성 페이지:
  - sources: [[bp_cc3351_evm_ug]] — 챕터 인덱스 + 추출 품질 메모 + lazy ingest 후보 목록
- 갱신:
  - `wiki/index.md` — `## teams/g/bp-cc3351` 섹션 신설
- 핵심 합의:
  - EVM UG 23p → 6 챕터 분할 (`ch00`–`ch05`). 포팅 핵심은 `ch02_hardware.md` — P1/P2 2×20핀 핀맵(Table 2-3/2-4), JTAG 헤더(Table 2-5/2-6), 전원, 클럭.
  - pymupdf4llm 1.27.2.3 추출. GFM 테이블·이미지 모두 정상.
- 파생 페이지 미생성 (lazy): `boosterpack_pinmap`, `jtag_header_bp_cc3351`, `power_rails_bp_cc3351`, `clocking_bp_cc3351` — lp-am263p 포팅 작업이 trigger할 때 생성.

---

## [2026-05-22] ingest | rx_control ADC 채널 매핑 + TEMP 라벨 swap 함정

- 트리거: 사용자 — "STM32에서 ADC 값 읽고 nRF로 보내고 Tx까지 가는 거 맞지? 평가보드 어느 핀에 어떻게 전압 넣어?"
- 소스:
  - `01_RX_control/RX_control.ioc` — ADC1 6채널 매핑, GPIO_Label, sampling
  - `Application/Src/app_adc.c` — `MX_ADC1_Init`, DMA1_Ch1 circular, `adc_conv()`
  - `Application/Src/common.c:157-172` — `adc_calc()` (raw → 0~3.3V만, 분압 미적용)
  - `Application/Inc/common.h:17-31` — Front-end R값 상수 + NTC 모델
  - `_shared/oled_tv_protocol.h:140-148` — `rx_adc_raw_data_t` 구조체 순서
- 발견 (라벨 swap 함정):
  - ioc GPIO_Label: PC4=`TEMP2_ADC`, PC5=`TEMP1_ADC`
  - 그러나 ADC rank 등록 순서 + DMA 버퍼 구조체 필드 순서로 인해 `sensing_data.stack_temp1` = PC4 = silkscreen `TEMP2_ADC`. 보드 라벨과 SW 필드명이 한 쪽 swap 상태.
  - 어느 쪽이 틀린지 (보드 vs SW)는 회로도/실측으로 결정 필요 → 후속.
- 발견 (스케일 미적용):
  - `common.h`에 분압/션트 R값과 NTC β 모델 정의는 있으나 `adc_calc()`는 raw→0~3.3V 단순 환산만. 따라서 `rx_module.rx_data.vrect` 등에 들어가는 값 = 핀 전압 그대로. 0.01V 스케일 uint16 wire 변환은 SPI 송신 코드(미독)에서 이뤄지는 것으로 추정.
- 생성/갱신:
  - 신규 concept [[adc_channel_map]] — 채널 표, swap 함정, 시험 가이드, 스케일 상수 표 + 미적용 사실
  - [[rx_control]] — UART 절 다음에 ADC 절 추가 (요약 + concept 페이지 링크)
  - [[index]] — Concepts에 adc_channel_map 등록
- 데이터 흐름 (위키에 박은 그림): `ADC pin → ADC1 (6ch, cont., DMA circular) → sensing_data → adc_calc → rx_module → SPI2 → SPIS1 → ESB → Tx`. 세 단계 모두 transparent.
- 후속 (페이지 미생성):
  - SPI 송신 코드에서 float → wire uint16 (0.01 스케일) 변환 지점 확인 — 별도 ingest 시 [[adc_channel_map]] §Front-end 절 갱신.
  - 회로도 ingest 후 TEMP1/TEMP2 라벨 swap 진위 결정.

---

## [2026-05-22] update | rx_control↔rx_ble SPI 핀맵·모드 정합 보강

- 트리거: 사용자 — "각자 핀은 어떻게 되있어?" → 매뉴얼/위키엔 커넥터 핀까지만 있고 양쪽 MCU GPIO·페리 인스턴스는 ingest 안 돼 있던 상태.
- 소스 확인:
  - STM32: `01_RX_control/RX_control.ioc` + `Application/Src/app_spi.c:16-29` (`MX_SPI2_Init`)
  - nRF: `02_RX_ble/Application/main.c:103-105, 467-475` + `_shared/oled_tv_protocol.h:69-72`
- 사실:
  - **STM32 SPI2 / PB12-15** (nCS=PB12 SW, SCK=PB13, MISO=PB14, MOSI=PB15). NSS_SOFT, 8-bit, MSB, /4 prescaler → 9.0 Mbps.
  - **STM32 모드 mode 2**: `CLKPolarity=HIGH`+`CLKPhase=1EDGE` → CPOL=1, CPHA=0.
  - **nRF SPIS1 / P0.22(CS)·P0.27(SCK)·P0.25(MOSI)·P0.26(MISO)**. `NRF_SPIS_MODE_2`로 STM32 측과 정합 확인.
  - DMA: STM32 측 TX=DMA1_Ch5, RX=DMA1_Ch4 (byte, NORMAL).
- 갱신 페이지:
  - [[rx_control]] SPI 절 — 페리(SPI2)·핀맵 표·모드·NSS_SOFT·DMA 추가
  - [[rx_ble_module]] CN3 표 — nRF GPIO 컬럼 추가, SPIS1 인스턴스/MODE_2/드라이버 버퍼 명명 함정 명시
- 핵심: nRF 드라이버에서 `tx_module_data_t`를 SPIS **RX 버퍼**로 넘기는 부분이 명명상 헷갈리는 지점 — "어디서 오는가" 기준이라 그렇다는 점을 위키에 박아둠.
- 후속 (미반영): `02_RX_ble`/`03_TX_ble` → ESB 전환 시 CN3 핀맵·모드는 유지 가정, 변경 시 본 페이지들 재갱신.

---

## [2026-05-22] revert | 직전 ESB 페이로드 ingest 철회 + 260513 매뉴얼을 ESB wire 사양으로 복권

- 트리거: 사용자 — "지금 보내준 데이터는 프로그래밍 상에서 데이터를 어떻게 관리할지에 관한 것들로 보임". 직전 ingest가 잘못된 가정 위에 세워졌음.
- 잘못된 가정 (직전 entry): `_shared/oled_tv_protocol.h`의 `tx_module_data_t` / `rx_module_data_t`를 무선 wire format으로 간주.
- 정정: 그 헤더는 **MCU 내부 데이터 모델** (센싱·상태값 관리용). **무선 wire format은 260513 매뉴얼이 정의한 11 B 패킷 (0x10/0x11/0x12 TX→RX, 0x50/0x51/0x52 RX→TX)**. 무선모듈이 transparent bridge라 SPI 11 B 프레임이 곧 무선 페이로드 — ESB 전환 후에도 동일.
- 삭제 페이지:
  - sources: `oled_tv_protocol_h.md`
  - concepts: `esb_payload_tx_to_rx.md`, `esb_payload_rx_to_tx_ack.md`
  - raw: `oled_tv_protocol.h` 사본
- 복원 페이지 (직전 historical 분리 되돌림):
  - [[spi_packet_format]] / [[tx_to_rx_packets]] / [[rx_to_tx_packets]] frontmatter에서 `historical, ble` 제거 + `esb` 태그 추가, 본문 상단 deprecation 노트 제거. `spi_packet_format`에 "ESB 매핑" 절 신설 (PTX/PRX 매핑, ACK payload 운용).
  - [[spi_protocol_manual_260513]] 소스 페이지의 historical 표시 제거, "이 11 B 프레임이 곧 end-to-end 무선 wire 사양"으로 단언.
  - [[rx_control]] SPI 절 원복.
  - `index.md` Historical 서브섹션 제거, 본 영역에 ESB 표시 추가.
- 핵심 교훈:
  - "wire format은 코드의 struct에 있다"고 가정하지 말 것. **수기 매뉴얼이 우선**이고, 코드 struct는 사내 구현 모델일 수 있음.
  - "데이터는 그대로"의 사용자 의미는 **매뉴얼 사양 유지**이지 코드 struct 유지가 아니었음.
- 후속 (페이지 미생성):
  - [[esb_link_layer]] — ESB 무선 파라미터 (역할/채널/주소/bitrate/ACK retry 등) 결정 시 환원.
  - [[nrf_bridge_design]] — nRF 펌웨어 내부 SPI↔ESB 브리지 동작/스케줄 (라운드로빈 vs 묶음).
  - `_shared/oled_tv_protocol.h`의 내부 모델 ↔ 11 B wire 사양 간 매핑(직렬화/역직렬화)이 코드에서 어떻게 구현되는지 — 필요 시 별도 ingest.

---

## [2026-05-22] ingest | OLED TV ESB 페이로드 사양 (BLE 시절 SPI 매뉴얼과 분리) — *REVERTED 2026-05-22*

> **REVERTED.** 위 revert entry 참조. 본 entry는 작업 이력 보존 목적으로만 남김.

- 트리거: 사용자 — "ble 통신을 esb 통신으로 바꿀 예정, 대신 보내는 데이터 자체는 그대로". ESB-TX↔ESB-RX 페이로드 결정 작업 중.
- 소스: `projects/c/oled_tv_software/_shared/oled_tv_protocol.h`
- raw 사본: `teams/c/oled_tv_software/raw/oled_tv_protocol.h`
- 생성 페이지:
  - sources: [[oled_tv_protocol_h]]
  - concepts: [[esb_payload_tx_to_rx]] (45 B), [[esb_payload_rx_to_tx_ack]] (56 B, ACK payload)
- 갱신 페이지:
  - [[rx_control]] — SPI 절을 ESB 기준으로 갱신, BLE 시절 페이지는 historical 링크로 분리
- Historical 분리 (이전 ingest의 가정 변경):
  - [[spi_packet_format]] / [[tx_to_rx_packets]] / [[rx_to_tx_packets]] frontmatter에 `historical, ble` 태그 추가, 본문 상단 deprecation 노트
  - 직전 ingest(260513) 때 "패킷 구조는 ESB에서도 유지"로 가정했지만 실제로는 전 항목이 바뀜: 11 B 고정→가변, 헤더 ID(0x10/0x50 등)→0xC0 단일, CRC→XOR, bit-packed Uint16(0.01 스케일)→struct float, 10 ms→20 ms.
- 핵심 합의:
  - **무선 계층만 교체, 데이터는 그대로**. SPI 브리지 프레임이 곧 ESB 페이로드 (transparent, 단편화 없음).
  - **ACK payload로 양방향**: PTX=ESB-TX(20ms 주기 마스터), PRX=ESB-RX. RX→TX는 PRX가 FIFO에 미리 적재 → PTX 다음 송신 때 piggyback. RX→TX 주기는 PTX에 종속.
  - **wire 호환의 본질**은 `#pragma pack(1)` + 모든 enum `__attribute__((__packed__))`. 두 페이지 모두 `_Static_assert(sizeof == ...)` 단정 권장.
  - 헤더 상단 주석/`RX_BLE_ADV_NAME` 매크로는 BLE 전제 표현 — 구조체는 transport 무관, 주석·매크로만 ESB 표현으로 갱신 필요.
- 후속 (페이지 미생성):
  - [[esb_link_layer]] — ESB 무선 파라미터 (역할/채널/주소/bitrate/ACK retry 등). 사내 결정 또는 SDK 예제 기반으로 결정되면 환원.
  - [[nrf_bridge_design]] — nRF 펌웨어 내부 SPI↔ESB 브리지 동작/버퍼링/타이밍.
  - `02_RX_esb` / `03_TX_esb` 코드는 아직 존재하지 않음 (`02_RX_ble` / `03_TX_ble`만 있음). 구현 시 ingest 대상.

---

## [2026-05-22] ingest+update | IS25LX256 device descriptor 검증 + 진단 트리 작성

- 트리거: 사용자 — "다음에 포팅 과정에서 '왜 이런 문제가 발생했고 무엇이 원인이고 어떻게 해결했더라?' 라는 관점으로 질문할 예정". 미래 자기 질문에 답이 되는 진입점 구조로 정리.
- 발견: IS25LX256 device descriptor 위치 확정
  - SysConfig JSON: `C:\ti\mcu_plus_sdk_am263px_26_00_00_01\source\sysconfig\board\.meta\flash\IS25LX256.json` (111 lines, SDK installer 동봉)
  - **GitHub `TexasInstruments/mcupsdk-core` public 미러에는 미공개** — `source/sysconfig/` 트리 전체가 제외됨. SDK 인스톨러에서만 얻을 수 있음.
- raw 사본 신설: `teams/g/lp-am263p/raw/mcupsdk/source/sysconfig/board/.meta/flash/IS25LX256.json`
- 디스크립터 검증 (datasheet 대조):
  - `rdIdSettings.dummy8 = 8` ✓ (ch08 Table 8.1, 8D-8D-8D RDID dummy=8)
  - `p888d.protoCfg.bitP = 231 (0xE7)` ✓ (ch06.5 VCR 0x00: E7h=Octal DDR with DQS)
  - `p888d.dummyCfg.bitP = 16` ✓ (ch06.5 VCR 0x01: 16 dummy cycles)
  - `p888d.cmdRd/cmdWr = 0x7C/0x84` ✓
  - `flashManfId=0x9D, flashDeviceId=0x5A19` ✓ (ISSI)
  - **디스크립터 자체는 datasheet와 완전 일치 → sweep 실패의 원인은 디스크립터가 아님**
- 갱신 페이지:
  - [[sbl_app_flash_handoff]] — "진단 트리" 절 신설. 사용자 관점("왜/원인/해결") 4가지 원인 후보 정리:
    1. Chip이 8D mode 진입 못 함 (skipHwInit 게이트 문제)
    2. `Flash_quirkSpansionUNHYSADisable` SysConfig 자동매핑 (가능성 높음)
    3. DQS 모드 불일치 (chip은 E7h DQS-on, OSPI 컨트롤러는 DQS-off일 때)
    4. ECC ON 상태에서 dummy table 불일치 (드뭄)
  - [[mcupsdk_flash_nor_ospi]] — "아직 안 읽은 것"에서 디스크립터 항목 ✓ 갱신 (위치 + 검증 결과)
  - [[is25lx256_vs_spansion_quirks]] §6.5 — 진단 트리 cross-link 추가
- 후속: SysConfig가 어디서 `params.quirksFxn`을 `Flash_quirkSpansionUNHYSADisable`에 연결하는지 — `ti_board_config.c` / `ti_board_open_close.c` 정독 시 처리

---

## [2026-05-22] update | `Flash_norOspiReadId` STIG dummy resolution 분석 보강

- 트리거: 사용자 sweep 디버깅 컨텍스트 — "SetModeDummy가 controller dummyClks=16 설정 후 ReadId 호출하면 STIG가 16으로 나가는가?"
- 분석 (flash_nor_ospi.c line 847-913 `Flash_norOspiReadId` + line 99-117 `Flash_norOspiCmdRead`):
  - `Flash_norOspiReadId`는 STIG dummy를 **controller register에서 inherit 하지 않음**. 함수 내부 local `dummyBits` 변수를 직접 STIG에 박는다.
  - non-8D: 항상 `dummyBits=0` (literal, line 858)
  - 8D-8D-8D: `dummyBits = idCfg->dummy8` (line 864) — devCfg->idCfg.dummy8 별도 필드
  - 결론: `OSPI_setCmdDummyCycles(16)` 호출 직후 ReadId 호출해도 STIG dummy는 16 아님. non-8D는 0, 8D는 idCfg.dummy8.
- 함의: `idCfg.dummy8`과 `protocolCfg.dummyClksCmd`는 device descriptor의 별도 필드. RDID는 idCfg.dummy8만 사용. 두 필드 일관성이 descriptor 작성자 책임.
- 8D ReadId 실패 시 capture delay sweep loop(line 1250-1255)으로는 보정 불가 — capture delay는 phase 보정, dummy는 cycle count 차이라 데이터 자체가 시프트.
- 갱신 페이지:
  - [[flash_open_sequence]] — 신규 §RDID dummy resolution (결정 로직, 두 dummy 필드 분리, capture sweep 보정 불가 이유), 위험 포인트에 RDID dummy field 항목 추가
  - [[sbl_app_flash_handoff]] — 정합성 깨짐 지점 §4 신설(idCfg.dummy8 불일치), 진단 절차 dump 대상 필드에 idCfg.dummy8 명시
- 후속: IS25LX256 device descriptor 파일 위치 확인 + idCfg.dummy8 실제 값이 8 (datasheet ch08 Table 8.1)과 일치하는지 검증 — 진행 중

---

## [2026-05-22] update | `Flash_quirkSpansionUNHYSADisable` SysConfig 자동매핑 함정 보강

- 트리거: 사용자가 sweep 디버깅 중 0x71/0x65 opcode를 driver에서 발견. 이 opcode들은 IS25LX256 Command Table(ch08.2)에 존재하지 않음 확인.
- 실측: `flash_nor_ospi.c` line 1374-1403 `Flash_quirkSpansionUNHYSADisable` 함수가 line 1381 `Flash_norOspiRegRead(0x65, 0x00800004)` (Spansion RDAR), line 1399 `Flash_norOspiRegWrite(0x71, 0x04, ...)` (Spansion WRAR)를 호출. 함수는 같은 파일 내에선 호출되지 않음 — caller는 SysConfig 생성 board init이라고 사용자 보고.
- ISSI 측 거동: ch08.1 line 9 "incorrect command → standby" 규칙에 따라 0x65/0x71 모두 디코드 되지 않음. read는 bus default(0xFF) 리턴 → UNHYSA bit가 "이미 1"로 잘못 판단 → write 스킵으로 운 좋게 no-op으로 끝나는 케이스가 흔함. 단 read가 0x00 리턴 시 0x71 write 시도 → WEL 상태 어긋날 위험.
- 갱신 페이지:
  - [[is25lx256_vs_spansion_quirks]] — §2에 ISSI "incorrect command → standby" 인용 추가, §6.5 신설 (SysConfig 자동매핑 함정 + 워크어라운드 + 검증법), 체크리스트에 항목 추가
  - [[mcupsdk_flash_nor_ospi]] — 라인 인덱스 1374-1403 항목에 opcode/주소/caller 정보 보강
- 후속 (미반영, 별도 ingest 후보):
  - **RDID(0x9F) 8D DDR 시퀀스 concept 페이지** — Table 8.1: addr bytes 0, dummy 8, 8-0-8 protocol. sweep 실패 진단 시 진입점.
  - SysConfig에서 IS25LX256 디스크립터의 quirk 매핑 실체 위치 (`Flash_DevConfig` 어느 필드인지) — `flash_nor_ospi.h` ingest 시 처리.

---

## [2026-05-22] ingest | TI MCU+ SDK `flash_nor_ospi.c` (Flash_open 시퀀스 + SBL 핸드오프)

- 소스: `https://github.com/TexasInstruments/mcupsdk-core` (branch `next`), commit `05d3aebbc8d6e9ef7fdb69a646c68676146ff5b5`, file `source/board/flash/ospi/flash_nor_ospi.c` (1429 lines)
- raw 사본: `teams/g/lp-am263p/raw/mcupsdk/source/board/flash/ospi/flash_nor_ospi.c`
- 생성 페이지:
  - sources: [[mcupsdk_flash_nor_ospi]] (라인 인덱스 + 후속 ingest 후보)
  - concepts: [[flash_open_sequence]], [[sbl_app_flash_handoff]]
- 트리거 질문: "SBL이 IS25LX256을 8D DDR로 올릴 때 쓴 dummy cycle, 종료 시 컨트롤러 상태" — prebuilt `.lib` 역분석 없이 소스 레벨에서 SBL → 앱 gap 식별 목적
- 핵심 합의:
  - **Dummy cycle 숫자는 이 파일에 없다** — `devCfg->protocolCfg.dummyClksRd/Cmd`에서 가져옴. 실제 값은 IS25LX256 디바이스 디스크립터(별도 파일, SBL board 패키지 혹은 SysConfig output). 후속 ingest 대상.
  - **`skipHwInit` 게이트가 SBL→앱 핸드오프 계약의 본질**: `TRUE`면 chip register write 전부 스킵, 컨트롤러 측 설정은 그대로 실행. 두 `Flash_DevConfig`가 bit-exact 일치해야 read 안 깨짐.
  - **PHY attack vector 자동 write가 destructive**: `skipHwInit`와 무관하게 PHY 경로는 항상 실행. attack vector 없으면 flash 마지막 sector를 erase+write. 양산 시 sector 사용 충돌 주의.
  - **Capture delay sweep으로는 dummy mismatch 보정 못 함** — capture delay는 phase 보정용, cycle count 다르면 데이터 자체가 shift됨.
  - `Flash_quirkSpansionUNHYSADisable` 실체가 line 1374에 있음 — [[is25lx256_vs_spansion_quirks]]의 quirk #1 보강 가능 (이번엔 미반영, 후속 lint 시 처리)
- 후속 ingest 후보 (페이지 미생성):
  - `flash_nor_ospi.h` 구조체 정의 (`FlashCfg_ProtoEnConfig`, `Flash_DevConfig`)
  - IS25LX256용 `Flash_DevConfig` 디스크립터 (실제 dummy/cmd/proto 값)
  - PHY tuning 동작 (`OSPI_phyReadAttackVector`, `OSPI_phyTuneDDR`)

---

## [2026-05-22] query→pages | IS25LX256 dummy cycle 표 & Spansion quirk 차이

- 사용자 작업 컨텍스트: **bp-3351 → AM263P 포팅** (메모리에 `project_lp_am263p.md` 기록)
- 질문 두 개를 raw에서 답하고 concept 페이지로 환원:
  1. **8D-8D-8D dummy cycle vs 주파수** — Table 6.7 (ch06 p.25-27)에서 직접 발췌. 16.67 MHz=3 cycles, 33.33 MHz=4 cycles. 3 variant(WX 200/ECC-OFF, WX 166/ECC-ON, LX 133) 별 차이 정리.
  2. **UNHYSA 비트 부재 확인** — 전 챕터 grep 결과 0건. ISSI는 sector arch가 ordering 옵션 `B`(factory 64KB)로 결정되고 런타임 토글 불가. Spansion CFR3V[UNHYSA] 가정 코드는 silent corruption 위험.
- 생성 페이지:
  - concepts: [[xspi_dummy_cycles]], [[is25lx256_vs_spansion_quirks]]
- 핵심 합의:
  - 데이터시트 표의 "16/33/...” 숫자는 200 MHz / N 그리드 (16=16.67, 33=33.33).
  - DLPRD dummy = Octal DDR dummy + 2 (학습 시 자주 잊는 +2).
  - 포팅 액션은 `is25lx256_vs_spansion_quirks` 끝의 체크리스트로 통합 — 향후 같은 충돌 의심 재발 시 진입점.

---

## [2026-05-22] ingest | IS25LX256 데이터시트 (raw 추출 + 인덱스)

- 소스: `C:\Users\echog\eta\25LX-WX256-128.pdf` (97쪽, ISSI Rev. A14 2026-05-12) — wiki 밖 보관
- raw 경로: `teams/g/lp-am263p/raw/IS25LX256/` — 12개 챕터 마크다운 + `img/` (PNG 52장)
- 도구: `pymupdf4llm` 1.27.2.3 (pip 설치). 챕터별 페이지 범위로 split 추출.
- 생성 페이지:
  - sources: [[is25lx256_datasheet]] (챕터 인덱스 + 추출 메타)
- 핵심 합의:
  - 97쪽 데이터시트를 한 번에 ingest하지 않는다. raw는 챕터 단위로 보관하고, 실제 작업이 트리거하는 챕터만 lazy하게 entities/concepts로 환원.
  - 이미지 추출 비용은 디스크만 차지 (토큰 0). Read tool로 PNG 열 때만 토큰 발생 → 필요한 그림만 lazy 로딩.
  - 테이블은 pymupdf4llm이 GFM 마크다운 테이블로 충분히 잘 보존 (Table 6.x 검증). 깨진 표는 ingest 단계에서 원본 PDF 재추출로 fallback.
- 새 프로젝트 디렉토리 신설: `teams/g/lp-am263p/` (CLAUDE.md 미작성 — 자산이 더 쌓이면 추가)

---

## [2026-05-21] ingest | 회로도 ingest 전략 (공통)

- 소스: 대화 — 회로도 파일을 wiki에 넘기는 방법 논의
- 생성 페이지:
  - concepts(공통): [[schematic_ingest_strategy]]
- 핵심 합의:
  - PDF 비전 처리는 토큰 과다 + 오인식률 문제로 피한다
  - EDA(Electronic Design Automation) 툴 텍스트 export가 1순위: 네트리스트(.net) + BOM(CSV)
  - PDF 텍스트 레이어 추출(pdftotext)이 2순위, 이미지 crop이 최후 수단
  - 파일명 규약: `YYYYMMDD-<프로젝트>-schematic__<블록명>.<ext>`
- 루트 `pages/` 디렉터리 신설: 프로젝트 비종속 공통 지식 위치

---

## [2026-05-21] ingest | OLED TV SPI 프로토콜 매뉴얼 (BLE 시절)

- 소스: 3개 CSV (`260513-oled_tv-protocol-manual__{introduction, from-eta_tx-to_etx_rx, from-eta_rx-to_etx_tx}.CSV`), 원본 CP949 → UTF-8 변환본 `.utf8.csv` 옆에 보관
- raw 경로: `teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__*.CSV`
- 생성 페이지:
  - sources: [[spi_protocol_manual_260513]]
  - entities: [[rx_ble_module]]
  - concepts: [[spi_packet_format]], [[tx_to_rx_packets]], [[rx_to_tx_packets]], [[comm_state_monitoring]]
- 갱신: [[rx_control]]에 SPI 페어 절 추가
- 핵심 합의:
  - 이 문서는 Rx Module ↔ Rx 무선모듈 간 **SPI 11-byte 패킷** 사양. 무선 구간(BLE→ESB)은 모듈 내부 처리이므로 SPI 패킷 골격은 ESB 전환 후에도 유지.
  - 페이지는 방향별로 묶음 (tx_to_rx / rx_to_tx).
  - BLE 시절 자산: `rx_ble_module`과 `sources` 페이지에만 `tags: [historical, ble]` 부여. 프로토콜 사양 페이지는 ESB와도 공유되므로 historical 태그 미부여.
- 원문 이슈 기록:
  - 0x50 Buffer[2] 비트 라벨 중복 (Bit.3 다회) — `Start Bit` 값으로 재정렬
  - 0x52 Power Stack#1·#2 온도 스케일 표기 불일치 (`0.1[℃]` vs `0.01[℃]`) — 예시값 역산상 둘 다 0.1 ℃ 추정, 구현 시 확인 필요

## [2026-05-21] ingest | RX_control PWM 개발 가이드

- 소스: `projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md` (2026-04-14 작성, `01_RX_control` 서브시스템)
- raw 복사본: `teams/c/oled_tv_software/raw/RX_control_PWM_가이드.md`
- 생성 페이지:
  - sources: [[rx_control_pwm_가이드]]
  - entities: [[rx_control]], [[tim8]], [[tim3]]
  - concepts: [[pwm_system]], [[dead_time]], [[trip_zone]], [[uart_command_set]]
- 핵심 합의: TIM3에 BDTR이 없어 시스템 전체가 SW CCR offset 방식 dead time으로 통일됨. `pwm_set_freq()` 후 ARR이 바뀌므로 `pwm_set_deadtime()` 재호출 필요.

## [2026-06-26] 갱신 | 8kw-ev-wpt-tx A3.5 HW 검증 — PPB 오버샘플 N=64 확정·main 머지

- **HW 노이즈 측정 결과 N=32 → N=64 상향 확정.** A3.5 △(노이즈 미측정) → ✓. 코드: `ETA_ADC_OVERSAMPLE_LOG2 = 6U`(eta_bsp_adc.h:28), main에 **PR #6 `d673e74`**로 머지(feature/adc-trigger-epwm0 3e5f117·4cffbe1·532e0eb).
- **파생 수치 N=64 재계산**: 출력/ISR 레이트 85032/64 = **1.33 kHz**(was 2.66), 노이즈 √64 = **÷8**(was ÷5.7), 그룹지연 (64−1)/2×11.76µs = **~370 µs**(was ~182).
- **갱신**: [[am263p_adc_ppb_averaging]](N=64·1.33kHz·÷8, §5 main 머지, △닫음), [[am263p_adc_rti_trigger]](§4 N=64), [[am263p_adc_instance_allocation]](§변환시간 예산 N=64 예시), [[adc]](A3.5 ✓·HW 확정), [[status]](직전완료·다음시작점=A4·구현현황 ✓·미결 #2 닫음·헤더 머지), [[roadmap]](adc 행 A3.5 ✓), index 1건.
- 변환시간 예산(≈315 ns)·repeater 미채택 근거는 불변 — N은 트리거에 걸쳐 누적이라 예산과 무관.
- ⚠️ 코드 잔재: eta_bsp_adc.h:23 doc 주석이 "(5 → N=32)" 예시로 남음(실제 매크로는 6U). 다음 코드 작업 시 정리 권장.

## [2026-06-26] 환원 | 8kw-ev-wpt-tx ADC 트리거 EPWM0_SOCA + PPB HW 평균 (branch feature/adc-trigger-epwm0)

- 출처: branch `feature/adc-trigger-epwm0` 코드(`3e5f117` 트리거 전환·`4cffbe1` PPB N=32·`532e0eb` N 손잡이) + AM263P TRM `ch07_5_controlss.md` + MCU+ SDK v2 `adc.h`·`etpwm.h`·`bootloader_soc.c`·`soc_rcm.h` 인용 재확인.
- **신설**: [[am263p_adc_ppb_averaging]] (lp-am263p concept; PPB HW 오버샘플 평균 정본 — 2의 거듭제곱 시프트 평균, OSINT ISR, SDK API 매핑, `selectPPBOSINTSource` 혼동주의, lockstep). [[am263p_adc_rti_trigger]] §4에서 분리.
- **갱신**: [[am263p_adc_instance_allocation]] — §변환시간 예산 신설(단일 변환≈315 ns: acq 85 ns=(ACQPS16+1)×5ns SYSCLK + conv 230 ns=11.5×ADCCLK20ns). △미검증(수치)을 정적 산정 확정으로 닫음(라이브 실측은 빈자리로 유지).
- **갱신**: [[am263p_adc_rti_trigger]] — 제목/intro를 RTI·EPWM 일반 트리거 정본으로 확장(파일명 보존, 개명 보류). §5 EPWM0_SOCA 경로 정본화(★RTI `enableIntr0` 함정 EPWM 미적용, ★실효 85 kHz=런타임 override). §4 PPB는 신설 페이지로 위임·△ 닫음. ADC1 라운드로빈 △ 확정.
- **갱신**: [[adc]] — A3.5 ✗→△(구현·부분검증), 구현 3커밋·repeater 미채택 근거·N 손잡이 기록, 지식 △ 닫고 노이즈 실측만 잔여. [[status]] — 다음 시작점(노이즈 실측)·직전 완료 신설·미결 #2 닫음·구현 현황표 A3.5 행 추가.
- **갱신**: [[build_methods]] — §6 신설: 산출물명 동일(.out/.mcelf, 디렉토리로 구분)·CCS 디버그는 .out만 필요(빌드 불요)·향후 빌드 통합+CCS 디버그 전용 방향.
- **갱신**: index 2건(allocation 변환시간·rti_trigger EPWM 보강 + ppb_averaging 신규 행).
- ★보정: 종전 구두 "window 80 ns"는 (ACQPS+1)×SYSCLK 공식상 **85 ns**(ACQPS=16). 단일 변환 ≈315 ns로 정정.

## [2026-06-25] 환원 | 8kw-ev-wpt-tx 펌웨어 4레이어 재구성 (PR #5)

- PR #5 (`feature/firmware-layering`, `0830b5f`·`9cd0181`) — BSP·HAL·ALG·App 전면 재구성, 동작 불변, 실보드 검증 통과.
- 신설: [[firmware_layering_8kw]] (아키텍처 정본 — 레이어 정의·의존 방향·네이밍·ALG 비어있는 이유·gui.py 비자명 결합 경고. 당시 파일명 `firmware_layering`, 2026-06-30 전사 표준 승격 시 `_8kw`로 리네임)
- 갱신: [[status]] — 소스 레이아웃·직전 완료·구현 현황표·다음 시작점
- 갱신: [[roadmap]] — firmware-layering task 행 추가·현재 위치
- 갱신: [[pc_monitor_gui]] — DEADTIME_H 경로·매크로명(ETA_DEADTIME_NS→ETA_BSP_PWM_DEADTIME_NS)·비자명 결합 경고 추가
- 갱신: [[gui_launch_architecture]] — write 단계 경로·매크로명 정정

## [2026-06-24] 결정 | 8kw-ev-wpt-tx 다음 작업 4건 (업무보고)

- 업무보고에서 확정한 다음 작업 우선순위 4건을 [[status]] 미결 사항 + `weekly_report_2026-06-17_23.md`에 기록.
  1. GUI 값 소수점 세 자리 표시 (`1.23 V`→`1.234 V`, `tools/gui/gui.py`)
  2. ADC 값 필터 추가 — 노이즈 널뛰기 해소. **SW vs MCU ADC 자체 기능(오버샘플링) 택일은 착수 시 판단**
  3. ADC SOC 트리거 RTI1(1 kSPS) → EPWM0(85 kHz) 전환 — PWM 로드맵 [[pwm]] P4 항목이 앞당겨진 것
  4. GUI 화면 녹화 — 최저 우선순위(nice-to-have)
- 항목 2·3 연계: 트리거 85 kHz 상승 후 고속 샘플 위에 필터 얹는 흐름. 필터 위치는 트리거 전환 후 노이즈 거동 보고 판단.
