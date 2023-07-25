package com.example.test_python_scripts;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EnableJpaRepositories("com.example.*")
@EntityScan("com.example.*")
public class TestPythonScriptsApplication {

    public static void main(String[] args) {
        SpringApplication.run(TestPythonScriptsApplication.class, args);
    }

}
