async function main() {
  // Provide the BareCoin contract address. You can set this via an environment variable or hardcode it temporarily.
  const bareCoinAddress = process.env.BARECOIN_ADDRESS || "0xYourBareCoinAddress";
  
  console.log("Deploying StakingGovernance with BareCoin address:", bareCoinAddress);

  const StakingGovernance = await ethers.getContractFactory("StakingGovernance");
  const stakingGovernance = await StakingGovernance.deploy(bareCoinAddress);
  await stakingGovernance.deployed();

  console.log("StakingGovernance deployed to:", stakingGovernance.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
