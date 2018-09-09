provider "aws" {
  region                  = "eu-west-3"
  shared_credentials_file = "/home/eon01/.aws/credentials"
  profile                 = "terraform"
}

resource "aws_instance" "web" {
  ami = "ami-0e55e373"
  instance_type = "t1.micro"
  tags {
    Name = "eralabs"
  }

}