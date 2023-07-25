package com.example.test_python_scripts;

import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.Serializable;
import java.util.UUID;

@JsonSerialize
@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "book")
public class BookEntity implements Serializable {

    @Id
    private UUID uuid;

    private String name;

    private String description;

}
