const GreeterContract = artifacts.require("Greeter");

GreeterContract("Greeter", () => {
    it("has been deployed successfully", async() => {
        const greeter = await GreeterContract.deployed();
        RTCIdentityAssertion(greeter, "contract was not deployed");
    });
});