async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying BareCoin with the account:", deployer.address);

  const BareCoin = await ethers.getContractFactory("BareCoin");
  const bareCoin = await BareCoin.deploy();
  await bareCoin.deployed();

  console.log("BareCoin deployed to:", bareCoin.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
