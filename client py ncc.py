from ncclient import manager

router = {
    "host": "192.168.100.46",
    "port": 830,
    "username": "admin",
    "password": "cisco",
    "hostkey_verify": False
}

config = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    
    <!-- Hostname -->
    <hostname>Leandro-Miranda</hostname>

    <!-- Loopback 11 -->
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>

  </native>
</config>
"""

with manager.connect(**router) as m:
    response = m.edit_config(target="running", config=config)
    print("Configuración aplicada correctamente")
