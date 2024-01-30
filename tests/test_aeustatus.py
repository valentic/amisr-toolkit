"""AEUStatus Unit Tests"""

import pytest

import amisr_toolkit as atk

def test_parse():
    raw = "5A 02 01 01 1A 51 00 C4 93 01 01 01 01FF 0292 0263 0182 00BA 00BA 02EE 0000 01AE8F8B FF 01 FF"
    status = atk.AEUStatus(raw)

    assert status.board_id == 90
    assert status.status_format == 2
    assert status.firmware_major == 1
    assert status.firmware_minor == 1
    assert status.firmware_patch == 26
    assert status.pulse_width_alarm == False
    assert status.sspa_overdrive_alarm == False
    assert status.sspa_overtemp_alarm == False
    assert status.sspa_overtemp_alarm_latch == False
    assert status.dew_sensor_alarm == True
    assert status.extended_funcs == False
    assert status.sspa_overcurrent_alarm == False
    assert status.signal_select == 0
    assert status.signal_count == [196, 147]
    assert status.signal_voltage == pytest.approx([1.9215686274509804, 1.4411764705882353])
    assert status.sspa_power_enabled == True
    assert status.sspa_gating_enabled == True
    assert status.interrupt_enabled == True
    assert status.p5v_voltage_monitor == pytest.approx(4.995112414467253)
    assert status.p8v_voltage_monitor == pytest.approx(7.331378299120234)
    assert status.m8v_voltage_monitor == pytest.approx(-7.298680351906162)
    assert status.sspa_voltage_monitor == pytest.approx(32.8494623655914)
    assert status.sspa_current_monitor == pytest.approx(2.1957728301213617)
    assert status.controller_temp == pytest.approx(40.90909090909091)
    assert status.sspa_temp == pytest.approx(40.90909090909091)
    assert status.interrupt_count == 28217227
    assert status.power_sample_delay == pytest.approx(63.75)
    assert status.power_sample_counts == 255
    assert status.bypass_enabled == True
    assert status.offset_enabled == True
    assert status.forced_enabled == False
    assert status.pfwd == pytest.approx(52.86056644880174)
    assert status.pref == pytest.approx(42.18518518518518)
    assert status.pwatts == pytest.approx(72.12995694645979)
    assert status.alarm_state == 0


def test_parse_none():
    raw = None 

    with pytest.raises(ValueError):
        status = atk.AEUStatus(raw)
       
def test_parse_empty():
    raw = "" 

    with pytest.raises(IndexError):
        status = atk.AEUStatus(raw)
        
def test_parse_partial():
    raw = "5A 02 01 01 1A 51" 

    with pytest.raises(IndexError):
        status = atk.AEUStatus(raw)
       
def test_parse_wrong_type():
    raw = "5B 02 01 01 1A 51" 

    with pytest.raises(ValueError):
        status = atk.AEUStatus(raw)
       
def test_parse_wrong_format():
    raw = "5A 20 01 01 1A 51" 

    with pytest.raises(ValueError):
        status = atk.AEUStatus(raw)
 

