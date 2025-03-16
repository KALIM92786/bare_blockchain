async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Deploy the BareCoin contract
  const BareCoin = await ethers.getContractFactory("BareCoin");
  const bareCoin = await BareCoin.deploy();
  await bareCoin.waitForDeployment();  // Use waitForDeployment() in ethers v6
  console.log("BareCoin deployed to:", await bareCoin.getAddress());

  // Deploy the StakingGovernance contract using the BareCoin address
  const StakingGovernance = await ethers.getContractFactory("StakingGovernance");
  const stakingGovernance = await StakingGovernance.deploy(await bareCoin.getAddress());
  await stakingGovernance.waitForDeployment();
  console.log("StakingGovernance deployed to:", await stakingGovernance.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
