async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  const StakingGovernance = await ethers.getContractFactory("StakingGovernance");
  const stakingGovernance = await StakingGovernance.deploy();

  await stakingGovernance.waitForDeployment();

  console.log("StakingGovernance deployed to:", await stakingGovernance.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
