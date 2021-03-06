import os
import subprocess
from loggers import log


def run_ffmpeg(progress_filename, uploaded_file_path, params, output_name):
    # If running locally, change this to the correct path.
    ffmpeg_path = '/home/h/bin/ffmpeg'

    os.makedirs('ffmpeg-progress', exist_ok=True)
    progress_file_path = os.path.join('ffmpeg-progress', progress_filename)
    log.info(progress_file_path)
    # Split params into a list as I want to use subprocess.run() with an array of arguments.
    params = params.split(' ')
    params.append(output_name)
    log.info(params)

    subprocess.run([ffmpeg_path, '-hide_banner', '-progress', progress_file_path, '-y', '-i', uploaded_file_path,
                    '-metadata', 'comment="free-av-tools.com"', '-metadata', 'encoded_by="free-av-tools.com"',
                    '-id3v2_version', '3', '-write_id3v1', 'true'] + params)


# AAC
def aac(progress_filename, uploaded_file_path, is_keep_video, fdk_type, fdk_cbr, fdk_vbr, is_fdk_lowpass,
        fdk_lowpass, output_path):
    # Keep the video (if applicable)
    if is_keep_video == "yes":
        ext = os.path.splitext(uploaded_file_path)[-1]
        output_ext = 'mp4' if ext == '.mp4' else '.mkv'
        # CBR
        if fdk_type == "fdk_cbr":
            if is_fdk_lowpass == "yes":
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -cutoff {fdk_lowpass} '
                           f'-b:a {fdk_cbr}k -c:s copy', f'{output_path}.{output_ext}')
            else:
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -b:a {fdk_cbr}k '
                           f'-c:s copy', f'{output_path}.{output_ext}')
        # VBR
        else:
            if is_fdk_lowpass == "yes":
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -cutoff {fdk_lowpass} '
                           f'-vbr {fdk_vbr} -c:s copy', f'{output_path}.{output_ext}')
            else:
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -vbr {fdk_vbr} '
                           f'-c:s copy', f'{output_path}.{output_ext}')

    # Audio-only output file
    else:
        output_ext = 'm4a'
        # CBR
        if fdk_type == "fdk_cbr":
            if is_fdk_lowpass == "yes":
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -cutoff {fdk_lowpass} '
                           f'-b:a {fdk_cbr}k', f'{output_path}.m4a')
            else:
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -b:a {fdk_cbr}k',
                           f'{output_path}.m4a')
        # VBR
        else:
            if is_fdk_lowpass == "yes":
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -cutoff {fdk_lowpass} '
                           f'-vbr {fdk_vbr}', f'{output_path}.m4a')
            else:
                run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -vbr {fdk_vbr}',
                           f'{output_path}.m4a')

    return output_ext


# AC3
def ac3(progress_filename, uploaded_file_path, is_keep_video, ac3_bitrate, output_path):
    # Keep video (if applicable)
    if is_keep_video == "yes":
        output_ext = 'mp4' if ext == '.mp4' else 'mkv'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a ac3 -b:a {ac3_bitrate}k -c:s copy',
                   f'{output_path}.{output_ext}')
    # Audio-only output file
    else:
        output_ext = 'ac3'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a ac3 -b:a {ac3_bitrate}k', f'{output_path}.ac3')

    return output_ext


# ALAC
def alac(progress_filename, uploaded_file_path, is_keep_video, output_path):
    # Keep video (if applicable)
    if is_keep_video == "yes":
        output_ext = 'mkv'
        run_ffmpeg(progress_filename, uploaded_file_path, '-c:v copy -c:a alac -c:s copy', f'{output_path}.mkv')
    # Audio-only output file
    else:
        output_ext = 'm4a'
        run_ffmpeg(progress_filename, uploaded_file_path, '-c:a alac', f'{output_path}.m4a')

    return output_ext


# CAF
def caf(progress_filename, uploaded_file_path, output_path):
    run_ffmpeg(progress_filename, uploaded_file_path, '-c:a alac', f'{output_path}.caf')
    output_ext = 'caf'
    return output_ext


# DTS
def dts(progress_filename, uploaded_file_path, is_keep_video, dts_bitrate, output_path):
    # Keep video (if applicable)
    if is_keep_video == "yes":
        output_ext = 'mkv'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a dca -b:a {dts_bitrate}k '
                   f'-c:s copy -strict -2', f'{output_path}.mkv')
    # Audio-only output file
    else:
        output_ext = 'dts'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a dca -b:a {dts_bitrate}k -strict -2',
                   f'{output_path}.dts')

    return output_ext


# FLAC
def flac(progress_filename, uploaded_file_path, is_keep_video, flac_compression, output_path):
    # Keep video (if applicable)
    if is_keep_video == "yes":
        output_ext = 'mkv'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a flac -compression_level {flac_compression} '
                   f'-c:s copy', f'{output_path}.mkv')
    # Audio-only output file
    else:
        output_ext = 'flac'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a flac -compression_level {flac_compression}',
                   f'{output_path}.flac')

    return output_ext


# MKA
def mka(progress_filename, uploaded_file_path, output_path):
    run_ffmpeg(progress_filename, uploaded_file_path, '-c:v copy -c:a copy', f'{output_path}.mka')
    output_ext = 'mka'
    return output_ext


# MKV
def mkv(progress_filename, uploaded_file_path, output_path):
    run_ffmpeg(progress_filename, uploaded_file_path, '-c copy -f matroska', f'{output_path}.mkv')
    output_ext = 'mkv'
    return output_ext

# MP3
def mp3(progress_filename, uploaded_file_path, is_keep_video, mp3_encoding_type, mp3_bitrate, mp3_vbr_setting,
        output_path):
    # Keep the video (if applicable)
    if is_keep_video == "yes":
        ext = os.path.splitext(uploaded_file_path)[-1]
        output_ext = 'mp4' if ext == '.mp4' else 'mkv'
        # CBR
        if mp3_encoding_type == "cbr":
            run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libmp3lame -b:a {mp3_bitrate}k',
                       f'{output_path}.{output_ext}')
        # ABR
        elif mp3_encoding_type == "abr":
            run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libmp3lame --abr 1 -b:a {mp3_bitrate}k',
                       f'{output_path}.{output_ext}')
        # VBR
        elif mp3_encoding_type == "vbr":
            run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libmp3lame -q:a {mp3_vbr_setting}',
                       f'{output_path}.{output_ext}')
    # Audio-only output file
    else:
        output_ext = 'mp3'
        if mp3_encoding_type == "cbr":
            run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a libmp3lame -b:a {mp3_bitrate}k',
                       f'{output_path}.mp3')
        elif mp3_encoding_type == "abr":
            run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a libmp3lame --abr 1 -b:a {mp3_bitrate}k',
                       f'{output_path}.mp3')
        elif mp3_encoding_type == "vbr":
            run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a libmp3lame -q:a {mp3_vbr_setting}',
                       f'{output_path}.mp3')

    return output_ext


# MP4
def mp4(progress_filename, uploaded_file_path, mp4_encoding_mode, crf_value, output_path):
    # Keep original codecs, simply change the container to MP4.
    if mp4_encoding_mode == "keep_codecs":
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c copy -f mp4 -movflags faststart', f'{output_path}.mp4')
    # Keep video codec, encode audio.
    elif mp4_encoding_mode == "keep_video_codec":
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libfdk_aac -vbr 5 -f mp4 '
                   f'-movflags faststart', f'{output_path}.mp4')
    # Encode video, keep audio codec.
    elif mp4_encoding_mode == 'convert_video_keep_audio':
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v libx264 -crf {crf_value} -c:a copy -f mp4 '
                   f'-movflags faststart', f'{output_path}.mp4')
    # Encode video and audio.
    else:
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v libx264 -preset {mp4_encoding_mode} -crf {crf_value} '
                   f'-c:a libfdk_aac -vbr 5 -f mp4 -movflags faststart', f'{output_path}.mp4')

    output_ext = 'mp4'
    return output_ext


# Opus
def opus(progress_filename, uploaded_file_path, opus_encoding_type, opus_vorbis_slider, opus_cbr_bitrate,
         output_path):
    # VBR
    if opus_encoding_type == "opus_vbr":
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libopus -b:a {opus_vorbis_slider}k',
                   f'{output_path}.opus')
    # CBR
    else:
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a libopus -vbr off -b:a {opus_cbr_bitrate}k',
                   f'{output_path}.opus')

    output_ext = 'opus'
    return output_ext


# Vorbis
def vorbis(progress_filename, uploaded_file_path, vorbis_encoding, vorbis_quality, opus_vorbis_slider, output_path):
    # ABR
    if vorbis_encoding == "abr":
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a libvorbis -b:a {opus_vorbis_slider}k',
                   f'{output_path}.ogg')
    # True VBR
    elif vorbis_encoding == "vbr":
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a libvorbis -q:a {vorbis_quality}', f'{output_path}.ogg')

    output_ext = 'ogg'
    return output_ext


# WAV
def wav(progress_filename, uploaded_file_path, is_keep_video, wav_bit_depth, output_path):
    # Keep the video (if applicable)
    if is_keep_video == "yes":
        output_ext = 'mkv'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:v copy -c:a pcm_s{wav_bit_depth}le -c:s copy',
                   f'{output_path}.mkv')
    # Audio-only output file
    else:
        output_ext = 'wav'
        run_ffmpeg(progress_filename, uploaded_file_path, f'-c:a pcm_s{wav_bit_depth}le', f'{output_path}.wav')

    return output_ext