(module
  (memory $m 1)
  (export "memory" (memory $m))

  (func $f1 (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l0 i32)
    (local.set $l0 (i32.const 0))
    (loop $loop_label
      (local $t i32)
      (local.set $t
        (i32.load8_u
          (i32.add (local.get $p0) (local.get $l0))
        )
      )
      (i32.store8
        (i32.add (local.get $p1) (local.get $l0))
        (local.get $t)
      )
      (local.set $l0
        (i32.add (local.get $l0) (i32.const 1))
      )
      (br_if $loop_label
        (i32.lt_u (local.get $l0) (local.get $p2))
      )
    )
  )
  (export "f1" (func $f1))
)

