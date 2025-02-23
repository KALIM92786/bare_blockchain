const { ethers } = require("hardhat");

async function main() {
  // Replace this with your actual deployed BareCoin address
  const rawBareCoinAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  // Convert to a checksummed address (this ensures ethers won't try to resolve it as an ENS name)
  const bareCoinAddress = ethers.getAddress(rawBareCoinAddress);
  
  const StakingGovernance = await ethers.getContractFactory("StakingGovernance");
  const stakingGovernance = await StakingGovernance.deploy(bareCoinAddress);
  await stakingGovernance.waitForDeployment();
  
  console.log("StakingGovernance deployed to:", await stakingGovernance.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
