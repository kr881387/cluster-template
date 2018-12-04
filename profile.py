# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

prefixForIP = "192.168.1."

link = request.LAN("lan")

for i in range(15):
  
  if i == 0:
    node = request.XenVM("head")
    node.routable_control_ip = "true"
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/head_setup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/head_setup.sh"))
    
    #install mpi
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
  
  elif i == 1:
    node = request.XenVM("metadata")
  
  elif i == 2:
    node = request.XenVM("storage")
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/storage_setup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/storage_setup.sh"))
    
  
  else:
    node = request.XenVM("compute-" + str(i-2))
    node.cores = 4
    node.ram = 4096
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/compute_setup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/compute_setup.sh"))
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/set_mpi_path.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/set_mpi_path.sh"))
  
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/passwordless.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
  
  # This code segment is added per Benjamin Walker's solution to address the StrictHostKeyCheck issue of ssh
  node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/ssh_setup.sh"))
  node.addService(pg.Execute(shell="sh", command="sudo -H -u ka837933 bash -c '/local/repository/ssh_setup.sh'"))
 
  node.addService(pg.Execute(shell="sh", command="sudo su ka837933 -c 'cp /local/repository/source/* /users/ka837933'"))
  
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
