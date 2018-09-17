resource "aws_rds_cluster_instance" "cluster_instances" {
  count = 1
  identifier = "aurora-cluster-demo1"
  cluster_identifier = "${aws_rds_cluster.default1.id}"
  instance_class = "db.t2.small"
  publicly_accessible = true
}

resource "aws_rds_cluster" "default1" {
  cluster_identifier = "aurora-cluster-demo1"
  availability_zones = ["us-east-1a","us-east-1b"]
  vpc_security_group_ids = ["${aws_security_group.mydbsg1.id}"]
  database_name = "mydb"
  master_username = "mydb1"
  master_password = "mydb12345"
}

resource "aws_security_group" "mydbsg1" {
  name = "mydbsg1"
  description = "RDS SG"
  vpc_id = "${var.rds_vpc_id}"

  # Only AUrora in
  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic.
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


provider "aws" {
  region = "${ var.region }"
}

output "RDS" {
   value = "${aws_rds_cluster_instance.cluster_instances.endpoint}"
}
