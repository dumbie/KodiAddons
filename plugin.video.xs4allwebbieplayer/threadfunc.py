import var

#Stop and reset all threads
def stop_reset_threads():
    var.thread_check_requirements.Stop()
    var.thread_zap_wait_timer.Stop()
    var.thread_update_television_program.Stop()
    var.thread_update_epg_program.Stop()
    var.thread_update_epg_channel.Stop()
    var.thread_update_playergui_info.Stop()
    var.thread_hide_playergui_info.Stop()
    var.thread_sleep_timer.Stop()
