package com.example.test_python_scripts;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@RestController
@RequestMapping("/book")
@RequiredArgsConstructor
public class BookController {

    private final BookRepository bookRepository;

    @GetMapping
    public List<BookEntity> getALl() {
        return bookRepository.findAll();
    }

    @PostMapping("/getByUuid")
    @ResponseBody
    public ResponseEntity<BookEntity> getById(@RequestBody GetByIdRequest request) {
        return ResponseEntity.ok(bookRepository.findById(request.getUuid()).orElse(null));
    }

    @NoArgsConstructor
    @Data
    public static class GetByIdRequest {
        private UUID uuid;
    }

}
