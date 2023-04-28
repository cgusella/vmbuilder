locals {
  timestamp        = formatdate("YYYY-MM", timestamp())
  output_directory = "${var.output_directory}/"
}

source "virtualbox-iso" "vbox" {
  boot_command = [ var.boot_command ]
  boot_wait            = "${var.boot_wait}"
  bundle_iso           = "${var.bundle_iso}"
  communicator         = "${var.communicator}"
  cpus                 = "${var.cpus}"
  memory               = "${var.memory}"
  disk_size            = "${var.disk_size}"
  format               = "${var.format}"
  guest_additions_mode = "${var.guest_additions_mode}"
  guest_os_type        = "${var.guest_os_type}"
  hard_drive_discard   = "${var.hard_drive_discard}"
  hard_drive_interface = "${var.hard_drive_interface}"
  headless             = "${var.headless}"
  host_port_max        = "${var.host_port_max}"
  host_port_min        = "${var.host_port_min}"
  http_directory       = "${var.http_directory}"
  http_port_max        = "${var.http_port_max}"
  http_port_min        = "${var.http_port_min}"
  iso_checksum         = "${var.iso_checksum}"
  iso_interface        = "${var.iso_interface}"
  iso_target_extension = "${var.iso_target_extension}"
  iso_target_path      = "${var.iso_directory}/${var.iso_file}"
  iso_urls = [
    "${var.iso_link}",
    "${var.output_directory}/${var.iso_file}"
  ]
  keep_registered              = "${var.keep_registered}"
  output_directory             = "${local.output_directory}"
  post_shutdown_delay          = "${var.post_shutdown_delay}"
  sata_port_count              = "${var.sata_port_count}"
  shutdown_command             = "echo '${var.ssh_password}' | sudo -E -S poweroff"
  shutdown_timeout             = "${var.shutdown_timeout}"
  skip_export                  = "${var.skip_export}"
  skip_nat_mapping             = "${var.skip_nat_mapping}"
  ssh_agent_auth               = "${var.ssh_agent_auth}"
  ssh_clear_authorized_keys    = "${var.ssh_clear_authorized_keys}"
  ssh_disable_agent_forwarding = "${var.ssh_disable_agent_forwarding}"
  ssh_file_transfer_method     = "${var.ssh_file_transfer_method}"
  ssh_handshake_attempts       = "${var.ssh_handshake_attempts}"
  ssh_keep_alive_interval      = "${var.ssh_keep_alive_interval}"
  ssh_username                 = "${var.ssh_username}"
  ssh_password                 = "${var.ssh_password}"
  ssh_port                     = "${var.ssh_port}"
  ssh_pty                      = "${var.ssh_pty}"
  ssh_timeout                  = "${var.ssh_timeout}"
  vboxmanage = [
    ["modifyvm", "{{ .Name }}", "--rtcuseutc", "off"],
    ["modifyvm", "{{ .Name }}", "--vram", "128"]
  ]
  virtualbox_version_file = "/tmp/.vbox_version"
  vm_name                 = "${var.vm_name}"
  vrdp_bind_address       = "${var.vnc_vrdp_bind_address}"
  vrdp_port_max           = "${var.vnc_vrdp_port_max}"
  vrdp_port_min           = "${var.vnc_vrdp_port_min}"
}

build {

  description = "Can't use variables here yet!"
  sources     = ["source.virtualbox-iso.vbox"]

  provisioner "shell" {
    binary            = false
    execute_command   = "echo '${var.ssh_password}' | {{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    expect_disconnect = true
    valid_exit_codes  = [0, 2]
    scripts = [
      # "scripts/init.sh",
      # "scripts/install/install-vb-guest-additions.sh",
      # "scripts/remove/remove-gnome.sh",
      # "scripts/install/install-plasma.sh",
      # "scripts/remove/remove-konqueror.sh",
      # "scripts/remove/remove-virtualbox.sh",
      # "scripts/install/install-sddm.sh",
      # "scripts/install/install-windowmanager.sh",
      # "scripts/install/install-terminator.sh",
      # "scripts/install/install-firefox.sh",
      # "scripts/install/install-gcc.sh",
      # "scripts/install/install-net-tools.sh",
      # "scripts/install/install-git.sh",
      # "scripts/install/install-ly.sh",
      # "scripts/install/install-vb-guest-utils.sh",
      # "scripts/clean.sh",
      # "scripts/prepare-for-upload.sh",
    ]
    start_retry_timeout = "${var.start_retry_timeout}"
  }

  provisioner "file" {
    sources = [
      "upload/bashrc",
      "upload/bashrc_root",
      "upload/config",
    ]
    destination = "/home/vagrant/upload/"
  }

  provisioner "shell" {
    binary            = false
    execute_command   = "echo '${var.ssh_password}' | {{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    expect_disconnect = true
    scripts = [
      "scripts/configure/config-vagrant-pass-less-sudoer.sh",
      "scripts/configure/config-bash-terminator-nano.sh",
      "scripts/configure/pin-them-to-taskbar.sh",
    ]
    start_retry_timeout = "${var.start_retry_timeout}"
  }

}
