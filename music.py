'''
Setup different listeners for same instrument to ensure possibility for 2 notes at the same time
'''


from psonic import *
import glob as glob
import os

base_dir = os.getcwd() + '/'

# instruments
synths = ['mod_beep', 'mod_pulse', 'mod_sine', 'growl']
#synths = ['hollow', 'dark_ambience', 'dull_bell', 'sine']
#synths = ['sine', 'sine', 'sine', 'sine']
#synths = ['piano', 'piano', 'piano', 'piano']
# synths = ['tech_saws', 'tech_saws', 'tech_saws', 'tech_saws']

# high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'tabla_tun1']
# low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'tabla_re']
# snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
snares = ['drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_phone1']
vox = ['ambi_choir']

BASS = [x for x in glob.glob('samples/BASS/*')]
HIGH_PERC = [x for x in glob.glob('samples/HIGH_PERC/*')]
LOW_PERC = [x for x in glob.glob('samples/LOW_PERC/*')]

#instruments = [synths, bass, low_percs, high_percs, synths, synths, high_percs, synths, bass, bass]


def get_sample_name(path):
    string = str(path)
    elem = string.split('/')[-1]
    sample_name = elem.replace('.wav', '')
    return sample_name


def setup_listeners():
    # setting up metronome
    run("""use_debug false
live_loop :metronome do
  cue :tick
  sleep 0.0625
end""")

    for synth in synths:
        # print("setting up listener for", synth)
        run(f"""in_thread do
  live_loop :{synth}, sync: :tick do
    n, c, a, r, p, m = sync "/osc/trigger/{synth}"
    with_fx :reverb, mix: m, room: 0.5, pre_amp: 0.1 do
      synth :{synth}, note: n, cutoff: c, attack: a, release: r, pan: p
    end
  end
end""")

    for bass in BASS:
        sample_name = get_sample_name(bass)
        # print(sample_name)
        # print('Setting up listener for: ', bass)
        run(f"""in_thread do
  live_loop :{sample_name}, sync: :tick do
    a, p = sync "/osc/trigger/{sample_name}"
    sample '{base_dir}{bass}', amp: a, pre_amp: 0.6, pitch: p
  end
end""")

    for perc in HIGH_PERC:
        sample_name = get_sample_name(perc)
        # print('Setting up listener for: ', perc)
        # print(sample_name)
        run(f"""in_thread do
  live_loop :{sample_name}, sync: :tick do
    a, m, m_echo, p = sync "/osc/trigger/{sample_name}"
    with_fx :echo, mix: m_echo, pre_mix: 0.2, phase: 1 do
      with_fx :reverb, mix: m, pre_amp: 0.3, room: 0.2 do
        sample '{base_dir}{perc}', amp: a, pitch: p, pre_amp: 0.7
      end
    end
  end
end""")

    for perc in LOW_PERC:
        sample = get_sample_name(perc)
        # print(sample)
        # print('Setting up listener for: ', sample)
        run(f"""in_thread do
  live_loop :{sample}, sync: :tick do
    a, p = sync "/osc/trigger/{sample}"
    sample '{base_dir}{perc}', amp: a, pre_amp: 0.3, pitch: p
  end
end""")


def play_sound(phenotype):
    """Play the sounds in sonic pi"""

    if 'bass' in phenotype['nature']:
        # print('Bass playing:  ', BASS[phenotype['instrument']])
        send_message(f"/trigger/{get_sample_name(BASS[phenotype['instrument']])}", phenotype['amp'], phenotype['pitch'])
    elif 'low_perc' in phenotype['nature']:
        # print('Low Perc: ', LOW_PERC[phenotype['instrument']])
        send_message(f"/trigger/{get_sample_name(LOW_PERC[phenotype['instrument']])}", phenotype['amp'], phenotype['pitch'])
    elif 'high_perc' in phenotype['nature']:
        # print(HIGH_PERC[phenotype['instrument']])
        send_message(f"/trigger/{get_sample_name(HIGH_PERC[phenotype['instrument']])}", phenotype['amp'], phenotype['mix_reverb'],
                     phenotype['mix_echo'], phenotype['pitch'])
    elif 'synth' in phenotype['nature']:
        # print('Synth: ', synths[phenotype['instrument']])
        send_message(f"/trigger/{synths[phenotype['instrument']]}", phenotype['note'], phenotype['cutoff'], phenotype['attack'],
                     phenotype['release'], phenotype['mix_reverb'])

    return


def stop_all_listeners():
    # Stop running processes in Sonic Pi
    stop()


