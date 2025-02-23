const { ethers } = require("hardhat");

async function main() {
  const BareCoin = await ethers.getContractFactory("BareCoin");
  const bareCoin = await BareCoin.deploy();
  await bareCoin.waitForDeployment();
  console.log("BareCoin deployed to:", await bareCoin.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
