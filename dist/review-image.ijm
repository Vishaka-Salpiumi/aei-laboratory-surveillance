// Teaching reference images only. Never infer patient quantity or resistance.
if (nImages == 0) exit("Open a downloaded reference image first.");
run("Duplicate...", "title=Review-copy");
run("8-bit");
run("Threshold...");
waitForUser("Review threshold", "Inspect the image and adjust threshold manually. Physical measurements require a verified pixel scale. Objects are not validated bacterial counts.");
