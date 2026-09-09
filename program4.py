system_state = {
    "network_available": True,
    "cpu_idle": False,
    "admin_override": False,
}

task_queue = []


def is_heavy_resource_ready():
    # Only triggered if preceding conditions pass due to lazy/short-circuit evaluation
    print("  [Lazy Probe] Checking hardware resource availability...")
    return True


def evaluate_task(task):
    rule = task["rule_type"]

    # Short-circuit logic: 'or' skips the right side if left is True;
    # 'and' skips the right side if left is False.
    if rule == "standard":
        return system_state["network_available"] and system_state["cpu_idle"]
    elif rule == "critical":
        return system_state["admin_override"] or (
            system_state["network_available"] and not system_state["cpu_idle"]
        )
    elif rule == "heavy":
        return (
            system_state["admin_override"]
            or (system_state["network_available"] and is_heavy_resource_ready())
        )
    else:
        return False


while True:
    print("\n--- Task Scheduler Menu ---")
    print("1. Add Task")
    print("2. Toggle System Flags")
    print("3. Run Scheduler (Lazy Eval)")
    print("4. View Status")
    print("5. Exit")

    choice = input("Select an option (1-5): ").strip()

    if choice == "1":
        name = input("Enter task name: ").strip()
        print("Select Condition Rule:")
        print("  a. Standard (network AND cpu_idle)")
        print("  b. Critical (admin_override OR (network AND NOT cpu_idle))")
        print("  c. Heavy (admin_override OR (network AND heavy_probe))")
        rule_choice = input("Choice (a/b/c): ").strip().lower()

        if rule_choice == "a":
            task_queue.append({"name": name, "rule_type": "standard"})
            print(f"Task '{name}' added with standard condition.")
        elif rule_choice == "b":
            task_queue.append({"name": name, "rule_type": "critical"})
            print(f"Task '{name}' added with critical condition.")
        elif rule_choice == "c":
            task_queue.append({"name": name, "rule_type": "heavy"})
            print(f"Task '{name}' added with heavy condition.")
        else:
            print("Invalid rule selected. Task discarded.")

    elif choice == "2":
        flag = input("Toggle which flag? (network / cpu / admin): ").strip().lower()
        if flag == "network":
            system_state["network_available"] = not system_state["network_available"]
            print(f"network_available set to: {system_state['network_available']}")
        elif flag == "cpu":
            system_state["cpu_idle"] = not system_state["cpu_idle"]
            print(f"cpu_idle set to: {system_state['cpu_idle']}")
        elif flag == "admin":
            system_state["admin_override"] = not system_state["admin_override"]
            print(f"admin_override set to: {system_state['admin_override']}")
        else:
            print("Unknown flag name.")

    elif choice == "3":
        if not task_queue:
            print("Queue is empty. No tasks to evaluate.")
        else:
            print("\nEvaluating queue...")
            remaining_tasks = []
            while task_queue:
                task = task_queue.pop(0)
                # Nested condition checking short-circuit execution result
                if evaluate_task(task):
                    print(f"  [EXECUTE] Task '{task['name']}' met criteria and ran.")
                else:
                    print(f"  [DEFER] Task '{task['name']}' criteria not met. Kept in queue.")
                    remaining_tasks.append(task)
            task_queue = remaining_tasks

    elif choice == "4":
        print(f"\nSystem State: {system_state}")
        print(f"Pending Tasks ({len(task_queue)}):")
        if task_queue:
            for idx, task in enumerate(task_queue, 1):
                print(f"  {idx}. {task['name']} [{task['rule_type']}]")
        else:
            print("  (None)")

    elif choice == "5":
        print("Shutting down task scheduler.")
        break

    else:
        print("Invalid selection. Please choose an option from 1 to 5.")